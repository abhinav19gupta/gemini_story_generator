import streamlit as st 
from story_generator import generate_story_from_images,narrate_story
from PIL import Image 


st.title('A.I story generator from images')
st.markdown('upload 1 to 10 images,choose a style and let AI write and narrate story for you') 

with st.sidebar:
    st.header('controls') 
    
    uploaded_files=st.file_uploader(
        'upload your images...',
        type=['png','jpeg','jpg'],
        accept_multiple_files=True
    ) 
    
    story_style=st.selectbox(
        'choose a story style',
        ['comedy','thriller','fairy tale','sci-fi','mystery','adventure','morale']
    )
    
    generate_button=st.button('generator story and narration',type='primary')
    
    
if generate_button:
    if not uploaded_files:
        st.warning('please upload atlest 1 image')
    elif len(uploaded_files)>10:
        st.warning('please upload an maximum of 10  images')
    else:
        with st.spinner('the A.I is writing and narrating your story.... this may take few times'):
            try:
                pil_images=[Image.open(uploaded_file) for uploaded_file in uploaded_files]
                st.subheader('your visual representation')
                image_columns=st.columns(len(pil_images))
                
                for i,image in enumerate(pil_images):
                    with image_columns[i]:
                        st.image(image,width='stretch')
                        
                generate_story=generate_story_from_images(pil_images,story_style)
                
                if 'Error' in generate_story or 'failed' in generate_story or 'Api_key' in generate_story:
                    st.error(generate_story)
                else:
                    st.subheader(f'your {story_style} story:')
                    st.success(generate_story)
                    
                st.subheader("Listen to your Story:")
                audio_file= narrate_story(generate_story)
                if audio_file:
                    st.audio(audio_file,format="audio/mp3")
                
            except Exception as e:
                st.error(f'an application error occurred {e}')
                