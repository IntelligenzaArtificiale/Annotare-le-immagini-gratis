import base64
import zipfile
import streamlit as st
import os
from streamlit_img_label_ita import st_img_label_ita
from streamlit_img_label_ita.manage import ImageManager, ImageDirManager


st.set_page_config(page_title="Annota gratis le tue immagini🖼", page_icon="🔍", layout='wide', initial_sidebar_state='auto')

st.markdown("<center><h1> Annota gratis le tue immagini🖼<small><br> Powered by INTELLIGENZAARTIFICIALEITALIA.NET </small></h1>", unsafe_allow_html=True)
st.write('<p style="text-align: center;font-size:15px;" > <bold>Crea annotazioni sulle tue immagini gratis, ed esportale in formato xml 📥<bold>  </bold><p><br>', unsafe_allow_html=True)



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



def run(img_dir):
    st.set_option("deprecation.showfileUploaderEncoding", False)
    idm = ImageDirManager(img_dir)

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
            #next_image() emoji frame: 

    def go_to_image():
        file_index = st.session_state["files"].index(st.session_state["file"])
        st.session_state["image_index"] = file_index

    def dowload_annotations():
        refresh()
        #print all .xml files in folder upload
        files = os.listdir(img_dir)
        xml_files = [f for f in files if f[-4:] == '.xml']
        print(xml_files)

        with st.expander("Scarica le Annotazioni 📥"):
            #create zip file with all annotations xml with zipfile
            zip_file = zipfile.ZipFile('annotations.zip', 'w')
            for file in os.listdir(img_dir):
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
            
            #delete all file in folder upload except Grazie.txt
            for file in os.listdir(img_dir):
                if file.endswith(".txt"):
                    pass
                else:
                    os.remove("Annotazioni Intelligenza Artificiale Italia/"+file)
                    #delete all session_state
                    for key in st.session_state.keys():
                        del st.session_state[key]



    # Sidebar: show status
    n_files = len(st.session_state["files"])
    n_annotate_files = len(st.session_state["annotation_files"])
    st.sidebar.write("🖼 Totale Immagini:", n_files)
    st.sidebar.write("🖼 Immagini Annotate:", n_annotate_files)
    st.sidebar.write("🖼 Immagini Rimanenti:", n_files - n_annotate_files)

    st.sidebar.write("\n\n\n")


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
        #st.sidebar.button(label="Aggiorna", on_click=refresh)

    st.sidebar.write("\n\n")
    cola, colb = st.sidebar.columns(2)
    cola.button(label="🖼 Prossima da annotare 🔃", on_click=next_annotate_file)
    if (( n_files - n_annotate_files) == 0):
        colb.button(label="📥 Scarica le annotazioni ⚙️", on_click=dowload_annotations)
    else:
        st.sidebar.info("📥 Annota tutte le immagini prima di scaricare le annotazioni ⚙️")

    #if n_files == 0 pass and return None
    if n_files == 0:
        st.warning("Nessuna immagine caricata")
        return None

    # Main content: annotate images
    img_file_name = idm.get_image(st.session_state["image_index"])
    img_path = os.path.join(img_dir, img_file_name)
    im = ImageManager(img_path)
    img = im.get_img()
    resized_img = im.resizing_img()
    resized_rects = im.get_resized_rects()
    rects = st_img_label_ita(resized_img, box_color="red", rects=resized_rects)

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

if __name__ == "__main__":
  
    uploaded_files = st.empty()
    # create a st.file_uploader to upload a multiple images
    uploaded_files = st.sidebar.file_uploader(
        "Carica le immagini da Annotare", type=["jpg", "png", "jpeg"], accept_multiple_files=True
    )

    #save the uploaded files to the folder "Annotazioni Intelligenza Artificiale Italia"
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            with open(os.path.join("Annotazioni Intelligenza Artificiale Italia", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
        # if the folder not is empty, run the app
        if len(os.listdir("Annotazioni Intelligenza Artificiale Italia")) > 0:
            css2 = """
            .exg6vvm0 {
                display: none;
            }
            """
            st.markdown(f'<style>{css2}</style>', unsafe_allow_html=True)
            run("Annotazioni Intelligenza Artificiale Italia")
            css2 = """
            .exg6vvm0 {
                display: block;
            }
            """
            st.markdown(f'<style>{css2}</style>', unsafe_allow_html=True)
        else:
            css2 = """
            .exg6vvm0 {
                display: block;
            }
            """
            st.markdown(f'<style>{css2}</style>', unsafe_allow_html=True)
            st.error("⚠️  Nessuna immagine caricata ⚠️")
            st.error("👈 Usa il menu a destra per caricare le immagini da annotare 🛑")
        
    
