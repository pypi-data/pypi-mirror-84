import cgi
import requests
import magic
import typer
import os
from .utils import compress, decompress, check_and_rename
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

app = typer.Typer()
url = 'https://api.bhej.dev'

@app.command()
def up(filename: str):
    try: 
        typer.echo(f"Compressing {filename}")
        file = compress(open(filename, 'rb').read())

        if len(file) > 1048576:
            typer.echo(f"Compressed file size too large. Files must be smaller than 1GB. Aborting.")
            raise typer.Exit(code=8)

        mime = magic.Magic(mime=True)
        files = {'upload_file': (filename, file, mime.from_file(filename))}
    except FileNotFoundError as err:
        typer.echo(f"No such file: '{filename}'. Aborting.")
        raise typer.Exit(code=3)
    except IsADirectoryError as err:
        typer.echo(f"'{filename}' is a directory. We currently don't support dir upload. Aborting.")
        raise typer.Exit(code=4)
    except Exception as err:
        typer.echo(f"Unexpected Error: {str(err)}")
        raise(err)

    typer.echo(f"Uploading {filename}")

    e = MultipartEncoder(fields=files)

    with tqdm(total=e.len,
              dynamic_ncols=True,
              unit='B',
              unit_scale=True) as bar:
        m = MultipartEncoderMonitor(e, lambda monitor: bar.update(monitor.bytes_read - bar.n))
        try:
            req = requests.post(url + '/upload', data=m, headers={'Content-Type': m.content_type})
        except Exception as err:
            typer.echo("Error in making network request. Check your network connection.")
            raise typer.Exit(code=6)

    if req.status_code == 500: 
        typer.echo("There was an unexpected server error. Please try again later.")
        raise typer.Exit(code=7)

    code = req.text
    link = f"{url}/file/{code}"

    typer.echo(f"Upload successful! Your code is -> {code}")
    typer.echo(f"You can also download the file directly at {link}")

    return 
    

@app.command()
def down(filecode: str, dest: str = '.'):
    # TODO: Add an option to change the file name? 

    if not os.path.exists(dest):
        typer.echo(f"No such location: {dest}. Aborting.")
        return

    if not os.path.isdir(dest):
        typer.echo(f"{dest} is not a directory. Aborting.")
        # TODO: Add a prompt to ask whether you'd like to create the dir.
        return

    dest = os.path.join(dest, '') # Adds trailing slash if missing.

    typer.echo(f"Downloading {filecode}")
    req = requests.get(url + '/download/' + filecode, stream=True)

    total_size_in_bytes= int(req.headers.get('Content-Length', 0))

    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, dynamic_ncols=True, unit='B', unit_scale=True)

    _, params = cgi.parse_header(req.headers['Content-Disposition'])

    filename = check_and_rename(params['filename'])

    fname = dest + filename
    gzname = fname + '.gz'

    with open(gzname, 'wb') as file:
        for data in req.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()
    
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print(progress_bar.n, total_size_in_bytes)
        print("ERROR, something went wrong")

    typer.echo(f"Downloaded {gzname}. Starting decompression.")

    with open(gzname, 'rb') as file:
        open(fname, 'wb').write(decompress(file.read()))

    os.remove(gzname)

    typer.echo(f"Done! Decompressed {filename}.")
