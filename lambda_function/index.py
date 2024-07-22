import os
from io import BytesIO
import tarfile
import boto3
import subprocess
import brotli
libre_office_install_dir = '/tmp/instdir'

s3 = boto3.client('s3')

def load_libre_office():
    if os.path.exists(libre_office_install_dir) and os.path.isdir(libre_office_install_dir):
        print('We have a cached copy of LibreOffice, skipping extraction')
    else:
        print('No cached copy of LibreOffice, extracting tar stream from Brotli file.')
        buffer = BytesIO()
        with open('/opt/lo.tar.br', 'rb') as brotli_file:
            d = brotli.Decompressor()
            while True:
                chunk = brotli_file.read(1024)
                buffer.write(d.decompress(chunk))
                if len(chunk) < 1024:
                    break
            buffer.seek(0)
        print('Extracting tar stream to /tmp for caching.')
        with tarfile.open(fileobj=buffer) as tar:
            tar.extractall('/tmp')
        print('Done caching LibreOffice!')
    return f'{libre_office_install_dir}/program/soffice.bin'
    
def convert_word_to_pdf(soffice_path, word_file_path, output_dir):
    conv_cmd = f"{soffice_path} --headless --norestore --invisible --nodefault --nofirststartwizard --nolockcheck --nologo --convert-to pdf:writer_pdf_Export --outdir {output_dir} {word_file_path}"
    response = subprocess.run(conv_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if response.returncode != 0:
        response = subprocess.run(conv_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response.returncode != 0:
            return False
    return True
    
def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Download the file from the source bucket
    source_file = f"/tmp/{file_key}"
    s3.download_file(bucket_name, file_key, source_file)

    # Check if the file is a .docx file
    if file_key.endswith('.docx'):
        # Convert the .docx file to PDF
        pdf_file = f"/tmp/{os.path.splitext(file_key)[0]}.pdf"
        
        # Upload the PDF file to the destination bucket
        output_dir = "/tmp"
        destination_bucket = os.environ['DESTINATION_BUCKET']
        destination_key = os.path.basename(pdf_file)
        
        soffice_path = load_libre_office()
        
        is_converted = convert_word_to_pdf(soffice_path, source_file, output_dir)
        if is_converted:
            s3.upload_file(pdf_file, destination_bucket, destination_key)
            # file_name, _ = os.path.splitext(base_name)
            # upload_to_s3(f"{output_dir}/{file_name}.pdf", bucket, f"{key_prefix}/{file_name}.pdf")
            return {"response": "file converted to PDF and available at same S3 location of input key"}
        else:
            return {"response": "cannot convert this document to PDF"}

        print(f"Successfully converted {file_key} to {destination_key} and uploaded to {destination_bucket}")
    else:
        print(f"Skipping {file_key} as it is not a .docx file")