# Hearsay

## World's best automatic subtitle generator

To run the backend, first run the following:
```bash
poetry install
```

Then, you can run the backend:
```bash
cd hearsay
poetry shell
python main.py
```

Then, you can open the webpage and use the system:
```
http://localhost:8000/web_page/index.html
```

Remember to also put your own AssemblyAI token into `hearsay/assembly/manager.py`
and install the Google Cloud SDK!