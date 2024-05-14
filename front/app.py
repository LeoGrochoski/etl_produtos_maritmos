import streamlit as st
from minio import Minio
from minio.error import S3Error
import os

def upload_file(uploaded_file):
    with open(os.path.join("temp_files", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getvalue())
    return os.path.join("temp_files", uploaded_file.name)

def save_to_minio(file_path):
    # Upload do arquivo para o MinIO
    minio_client = Minio(
        "localhost:9000",
        access_key="",
        secret_key="",
        secure=False
    )

    bucket_name = "landing"
    object_name = os.path.basename(file_path)

    try:
        minio_client.fput_object(bucket_name, object_name, file_path)
        file_url = f"http://localhost:9000/{bucket_name}/{object_name}"
        return file_url
    except S3Error as e:
        print(f"Erro ao salvar arquivo no Banco: {e}")

def main():
    st.title("Upload de Arquivo no banco")
    uploaded_file = st.file_uploader("Escolha um arquivo CSV ou JSON", type=["csv", "json"])

    if uploaded_file is not None:
        file_path = upload_file(uploaded_file)
        file_url = save_to_minio(file_path)
        st.write("Arquivo enviado com sucesso!")
        st.write(f"Link para download do arquivo: {file_url}")

if __name__ == "__main__":
    # Criar diretório temporário para salvar os arquivos temporários
    os.makedirs("temp_files", exist_ok=True)
    main()
