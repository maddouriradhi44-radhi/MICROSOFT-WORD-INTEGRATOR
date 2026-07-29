def on_login_success(user_info):
    from app.ui.home import HomePage
    home_window = HomePage(user_info=user_info, on_open_document=on_document_opened)
    home_window.resize(900, 700)
    home_window.show()

def on_document_opened(doc_name):
    print(f"→ Ouverture du document : {doc_name}")
    # ici : instancier document_view.py plus tard