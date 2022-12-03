import base64
import zipfile
import streamlit as st
import os
from streamlit_img_label import st_img_label
from streamlit_img_label.manage import ImageManager, ImageDirManager



st.set_page_config(page_title="Annota gratis le tue immagini🖼", page_icon="🔍", layout='wide', initial_sidebar_state='auto')

st.markdown("<center><h1> Annota gratis le tue immagini🖼<small><br> Powered by INTELLIGENZAARTIFICIALEITALIA.NET </small></h1>", unsafe_allow_html=True)
st.write('<p style="text-align: center;font-size:15px;" > <bold>Crea annotazioni sulle tue immagini gratis, ed esportale in formato xml 📥<bold>  </bold><p><br>', unsafe_allow_html=True)


st.set_option("deprecation.showfileUploaderEncoding", False)


hide_st_style = """
			<style>
			#MainMenu {visibility: hidden;}
			footer {visibility: hidden;}
			header {visibility: hidden;}
            .css-184tjsw p {
                word-break: break-word;
                font-size: 25px;
                font-weight: 800;
                text-align: center;
                color: darkgreen;
            }
            .css-629wbf {
                display: inline-flex;
                -webkit-box-align: center;
                align-items: center;
                -webkit-box-pack: center;
                justify-content: center;
                font-weight: 400;
                padding: 0.25rem 0.75rem;
                border-radius: 0.25rem;
                margin: 0px;
                line-height: 1.6;
                color: inherit;
                width: 100%;
                user-select: none;
                background-color: rgb(249, 249, 251);
                border: 1px solid rgba(49, 51, 63, 0.2);
            }
            .css-1x8cf1d {
                display: inline-flex;
                -webkit-box-align: center;
                align-items: center;
                -webkit-box-pack: center;
                justify-content: center;
                font-weight: 400;
                padding: 0.5rem 0.75rem;
                border-radius: 0.25rem;
                margin: 0px;
                line-height: 1.8;
                color: inherit;
                width: 100%;
                user-select: none;
                background-color: rgb(255, 255, 255);
                border: 1px solid rgba(49, 51, 63, 0.2);
            }
			</style>
			"""
st.markdown(hide_st_style, unsafe_allow_html=True)



with st.sidebar.form("my-form", clear_on_submit=True):
    with st.expander("📂 Carica le tue immagini", expanded=True):
        uploaded_files = st.file_uploader(
        ".", type=["jpg", "png", "jpeg"], accept_multiple_files=True
            )
    submitted = st.form_submit_button("Carica le Immagini 🖼")

#save the uploaded files to the folder "Annotazioni Intelligenza Artificiale Italia"
if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        with open(os.path.join("Annotazioni Intelligenza Artificiale Italia", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())


if len(os.listdir("Annotazioni Intelligenza Artificiale Italia")) > 1:
            
    idm = ImageDirManager("Annotazioni Intelligenza Artificiale Italia")

    if "files" not in st.session_state:
        st.session_state["files"] = idm.get_all_files()
        st.session_state["annotation_files"] = idm.get_exist_annotation_files()
        st.session_state["image_index"] = 0
    else:
        idm.set_all_files(st.session_state["files"])
        idm.set_annotation_files(st.session_state["annotation_files"])

    def refresh():
        st.session_state["files"] = idm.get_all_files()
        st.session_state["annotation_files"] = idm.get_exist_annotation_files()
        st.session_state["image_index"] = 0

    def next_image():
        image_index = st.session_state["image_index"]
        if image_index < len(st.session_state["files"]) - 1:
            st.session_state["image_index"] += 1
        else:
            st.warning('This is the last image.')

    def previous_image():
        image_index = st.session_state["image_index"]
        if image_index > 0:
            st.session_state["image_index"] -= 1
        else:
            st.warning('This is the first image.')

    def next_annotate_file():
        image_index = st.session_state["image_index"]
        next_image_index = idm.get_next_annotation_image(image_index)
        if next_image_index:
            st.session_state["image_index"] = idm.get_next_annotation_image(image_index)
        else:
            st.success(" 🎁 Tutte le immagini sono state Annotate 🎁")
            st.success(" 👈 Scarica il file xml con le annotazioni dal menu a destra 📥")
            st.balloons()

    def go_to_image():
        file_index = st.session_state["files"].index(st.session_state["file"])
        st.session_state["image_index"] = file_index

    def dowload_annotations():
        refresh()
        #print all .xml files in folder upload
        files = os.listdir("Annotazioni Intelligenza Artificiale Italia")
        xml_files = [f for f in files if f[-4:] == '.xml']
        print(xml_files)

        with st.expander("Scarica le Annotazioni 📥"):
            #create zip file with all annotations xml with zipfile
            zip_file = zipfile.ZipFile('annotations.zip', 'w')
            for file in os.listdir("Annotazioni Intelligenza Artificiale Italia"):
                if file.endswith(".xml"):
                    zip_file.write("Annotazioni Intelligenza Artificiale Italia/"+file)
                #add also file Grazie.txt
            zip_file.write("Grazie.txt")
            zip_file.close()

            #download zip file
            with open('annotations.zip', 'rb') as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                href = f'<a href="data:file/zip;base64,{b64}" download="Annotazioni Intelligenza Artificiale Italia.zip"> 👉  🎁Scarica Gratis le Annotazioni🎁 👈 </a>'
                st.markdown(href, unsafe_allow_html=True)

            #delete all session_state
            for key in st.session_state.keys():
                st.session_state.pop(key)

            #delete all file in folder upload except Grazie.txt
            for file in os.listdir("Annotazioni Intelligenza Artificiale Italia"):
                #se il file non termina con txt
                if file[-4:] != '.txt':
                    os.remove("Annotazioni Intelligenza Artificiale Italia/"+file)
            refresh()
            st.experimental_rerun() #restart app
        
    def delete_annotations():
        for key in st.session_state.keys():
            st.session_state.pop(key)

        #delete all file in folder upload except Grazie.txt
        for file in os.listdir("Annotazioni Intelligenza Artificiale Italia"):
            if file[-4:] != '.txt':
                    os.remove("Annotazioni Intelligenza Artificiale Italia/"+file)

        refresh()
        st.experimental_rerun()

            

    # Sidebar: show status
    st.sidebar.write("\n\n")
    n_files = len(st.session_state["files"])
    n_annotate_files = len(st.session_state["annotation_files"])
    st.sidebar.write("🖼 Totale Immagini:", n_files)
    st.sidebar.write("🖼 Immagini Annotate:", n_annotate_files)
    st.sidebar.write("🖼 Immagini Rimanenti:", n_files - n_annotate_files)
    st.sidebar.write("\n\n")
    st.sidebar.selectbox(
        "🖼 Immagini caricate",
        st.session_state["files"],
        index=st.session_state["image_index"],
        on_change=go_to_image,
        key="file",
    )
    st.sidebar.write("\n\n")
    st.sidebar.subheader(" ⚙️ COMANDI ⚙️ ")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.button(label="⏪ 🖼 ", on_click=previous_image)
    with col2:
        st.button(label=" 🖼 ⏩ ", on_click=next_image)

    col3, col4 = st.sidebar.columns(2)
    with col3:
        st.sidebar.button(label="🖼 Prossima da annotare 🖼", on_click=next_annotate_file)

    with col4:
        st.sidebar.button(label="🔃 Refresh 🔃", on_click=refresh)

    st.sidebar.button(label="📥 Scarica le annotazioni 📥", on_click=dowload_annotations)
    st.sidebar.button(label="🗑 Elimina tutto 🗑", on_click=delete_annotations)

    try:
        # Main content: annotate images
        img_file_name = idm.get_image(st.session_state["image_index"])
        img_path = os.path.join("Annotazioni Intelligenza Artificiale Italia", img_file_name)
        im = ImageManager(img_path)
        img = im.get_img()
        resized_img = im.resizing_img()
        resized_rects = im.get_resized_rects()
        rects = st_img_label(resized_img, box_color="red", rects=resized_rects)
        

        def annotate():
            im.save_annotation()
            image_annotate_file_name = img_file_name.split(".")[0] + ".xml"
            if image_annotate_file_name not in st.session_state["annotation_files"]:
                st.session_state["annotation_files"].append(image_annotate_file_name)
            next_annotate_file()

        if rects:
            preview_imgs = im.init_annotation(rects)

            for i, prev_img in enumerate(preview_imgs):
                prev_img[0].thumbnail((200, 200))
                col1, col2 = st.columns(2)
                with col1:
                    col1.image(prev_img[0])
                with col2:
                    select_label = col2.text_input("Etichetta", key=f"label_{i}")

                    im.set_annotation(i, select_label)

            st.button(label="✅ Salva e passa all'immagine successiva 👉🖼", on_click=annotate)
    
    except Exception as e:
        st.error("Qualcosa è anda storto, prova a ricaricare la pagina")
        print(e)
    
else:
    
    st.error("⚠️  Nessuna immagine caricata ⚠️")
    st.error("👈 Usa il menu a destra per caricare le immagini da annotare 🛑")



