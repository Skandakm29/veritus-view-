import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import chat_gpt  
import navigation
import face
import speak_to_text

# Set page configurations
st.set_page_config(layout="wide", page_title="Veritas View", page_icon="🔍")

# Custom CSS for layout and style
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Title Section with Gradient Text
st.markdown("""
    <style>
    .gradient-text {
        font-weight: bold;
        background: -webkit-linear-gradient(left, #ff5733, #ffc300, #ffffff);
        background: linear-gradient(to right, #ff5733, #ffc300, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline;
        font-size: 3em;
        margin-bottom: 0px;
    }
    </style>
    <div class="gradient-text">Veritas View</div>
    """, unsafe_allow_html=True)

# Sidebar for navigation and sections
class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        with st.sidebar:
            # Sidebar typing animation
            typing_animation = """
            <h3 style="text-align: left;">
            <img src="https://readme-typing-svg.herokuapp.com/?font=Righteous&size=35&Left=true&vLeft=true&width=500&height=70&lines=Veritas++View🔍" alt="Typing Animation" />
            </h3>
            """
            st.markdown(typing_animation, unsafe_allow_html=True)
            st.sidebar.write("")  # For spacing

            # Navigation menu
            app = option_menu(
                menu_title='Sections',
                options=['Home', 'Object Detection📷', 'Ai chatbot', 'Insights🔬', 'Settings⚙️','Study assistance'],
                default_index=0,
            )

            # Developer info in the sidebar
            linkedin_url = "https://www.linkedin.com/in/k-m-skanda-541a02291/"
            linkedin_link = f"[Circuit Surge]({linkedin_url})"
            st.sidebar.header(f"Developed by {linkedin_link}")
            return app

# Instantiate the multi-page app framework
multi_app = MultiApp()

# Define navigation for each section
selected_page = multi_app.run()

# Home Page Content
if selected_page == "Home":
    st.write(":orange[Seeing the truth through AI-powered object detection and analysis.]")
    st.image('C:\Smart glass\man-wearing-hightech-smart-glasses-searches-block-chain-icon-distributed-computing-system-with-businessman-s-hand-grasping-icon-using-generative-ai-2000x1121.jpg')
    st.write('Veritas View harnesses the power of computer vision and AI to deliver precise object detection and insightful analytics. Our platform enables users to explore visual data with advanced detection algorithms tailored for real-time use cases.')

    # Slideshow section
    col4, col5, col7, col6, col8, col9, col10 = st.columns([0.03, 0.45, 0.03, 0.6, 0.03, 0.40, 0.02])
    with col5:
        st.write(' ')
        components.html("""
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        .mySlides { display: none; }
        img { vertical-align: middle; width: 100%; margin: 0; padding: 0; }
        .slideshow-container { max-width: 400px; max-height: 400px; position: 100%; margin: 0; }
        .numbertext { color: #f2f2f2; font-size: 12px; padding: 8px 12px; position: absolute; top: 0; }
        .fade { animation-name: fade; animation-duration: 1.9s; }
        @keyframes fade { from {opacity: .4} to {opacity: 1} }
        </style>
        </head>
        <body>
        <script>
          let slideIndex = 0;
          showSlides();
          function showSlides() {
            let i;
            let slides = document.getElementsByClassName("mySlides");
            for (i = 0; i < slides.length; i++) { slides[i].style.display = "none"; }
            slideIndex++;
            if (slideIndex > slides.length) { slideIndex = 1 }
            slides[slideIndex-1].style.display = "block";
            setTimeout(showSlides, 2000); 
          }
        </script>
        </body>
        </html>
        """, height=300, width=400)

# Object Detection Page Content
elif selected_page == "Object Detection📷":
    st.title("Object Detection")
    st.write("This section allows you to upload images for real-time object detection.")
    # Add object detection functionality

# AI Chatbot Page Content
elif selected_page == "Ai chatbot":
    st.title("AI Chatbot")
    st.write("Interact with the AI Chatbot below:")
    chat_gpt.run_streamlit_app()  # Ensure the function exists in the chat_gpt module

# Insights Page Content
elif selected_page == "Insights🔬":
    st.title("Insights and Analysis")
    st.write("Detailed breakdown of detected objects with relevant metrics and insights.")
    # Add insights functionality

# Settings Page Content
elif selected_page == "Settings⚙️":
    st.title("Settings")
    
    st.subheader("User Preferences")
    st.write("Customize your experience with the following options:")
    
    # Example settings
    enable_notifications = st.checkbox("Enable Notifications", value=True)
    preferred_language = st.selectbox("Select Preferred Language", ["English", "Spanish", "French", "German"])
    st.write("Selected Language:", preferred_language)
    
    if enable_notifications:
        st.success("Notifications are enabled.")
    else:
        st.warning("Notifications are disabled.")
    
    st.subheader("Advanced Settings")
    enable_logging = st.checkbox("Enable Logging", value=False)
    
    if enable_logging:
        st.success("Logging is enabled.")
    
    if st.button("Save Settings"):
        st.success("Settings have been saved successfully!")
        
# Study Page Content
# Study Page Content
elif selected_page == "Study assistance":
    st.title("Helping the Blind with Study Assistance")
    st.write("This section provides tools to assist visually impaired users in their studies.")
    
    # Add a link for further resources
    st.markdown("[Click here for study resources](https://example.com)")
    speak_to_text.capture_image_and_perform_ocr()
