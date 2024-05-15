import pipelines.etl_csv as etl_csv
import pipelines.etl_json as etl_json
import pandas as pd

dados_csv = etl_csv.main()
dados_json = etl_json.main()

try: 
    produtos = pd.concat([dados_csv, dados_json], ignore_index=True)
    print(produtos)
except None:
    print("Os dados estão vindo como none, verificar estração e processamento dos dados")
    
