def stream_copy(src_path, dst_path, chunk_size=8192):
    with open(src_path, "rb") as src, open(dst_path, "wb") as dst:
        while True:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            dst.write(chunk)



# django
def upload_large_file(request):
    with open("/tmp/uploaded_file", "wb") as dest:
        for chunk in request.FILES["file"].chunks():
            dest.write(chunk)
