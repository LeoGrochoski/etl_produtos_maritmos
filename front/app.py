import streamlit as st
from minio import Minio
from minio.error import S3Error
import os

def upload_file(uploaded_file):
    with open(os.path.join("temp_files", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getvalue())
    return os.path.join("temp_files", uploaded_file.name)

def save_to_minio(file_path, access_key, secret_key, bucket_name):
    # Upload do arquivo para o MinIO
    minio_client = Minio(
        "localhost:9000",
        access_key=access_key,
        secret_key=secret_key,
        secure=False
    )

    object_name = os.path.basename(file_path)

    try:
        minio_client.fput_object(bucket_name, object_name, file_path)
        file_url = f"http://localhost:9000/{bucket_name}/{object_name}"
        return file_url
    except S3Error as e:
        print(f"Erro ao salvar arquivo no Banco MinIO: {e}")
        return None

def main():
    st.title("Upload de Arquivo para Banco MinIO")
    
    # Solicitando ao usuário que insira o login
    login = st.text_input("Chave de Acesso")
    
    # Solicitando ao usuário que insira a senha
    senha = st.text_input("Chave Secreta", type="password")
    
    # Solicitando ao usuário que insira o nome do diretório
    diretorio = st.text_input("Nome do Bucket")

    uploaded_file = st.file_uploader("Escolha um arquivo CSV ou JSON", type=["csv", "json"])

    if st.button("Enviar"):
        if login and senha and diretorio and uploaded_file is not None:
            file_path = upload_file(uploaded_file)
            file_url = save_to_minio(file_path, login, senha, diretorio)
            
            if file_url:
                st.success("Arquivo enviado com sucesso!")
            else:
                st.error("Falha ao enviar o arquivo para o Banco.")
        else:
            st.error("Por favor, preencha todos os campos e selecione um arquivo.")

if __name__ == "__main__":
    os.makedirs("temp_files", exist_ok=True)
    main()
