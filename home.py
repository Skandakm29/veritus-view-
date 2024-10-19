import streamlit as st

def app():
    # Custom CSS styles
    st.markdown("""
        <style>
            .gradient-text {
                font-weight: bold;
                background: linear-gradient(to right, #4fc3f7, #07539e);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 3em;
                text-align: center;
                margin-bottom: 20px;
            }
            .typing-animation {
                text-align: center;
            }
            .features {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                margin: 10px;
            }
            h3 {
                color: #07539e;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # Gradient Text Header
    st.markdown('<div class="gradient-text">Welcome to Veritas View</div>', unsafe_allow_html=True)
    st.write(":orange[Your vision companion, enhancing accessibility through cutting-edge object detection and real-time feedback.]")

    # Add a high-quality image
    st.image("C:\Smart glass\man-wearing-hightech-smart-glasses-searches-block-chain-icon-distributed-computing-system-with-businessman-s-hand-grasping-icon-using-generative-ai-2000x1121.jpg", use_column_width=True)

    st.write("Veritas View uses AI-driven object detection and text-to-speech technology to aid the visually impaired by providing real-time environment analysis and personalized feedback.")
    
    # Typing animation
    typing_animation = """
        <h3 class="typing-animation">
        <img src="https://readme-typing-svg.herokuapp.com/?font=Righteous&size=35&Left=true&vLeft=true&width=500&height=47&lines=Empowering++Through++Vision🔍" alt="Typing Animation" />
        </h3>
    """
    st.markdown(typing_animation, unsafe_allow_html=True)

    # Features section
    st.subheader(":orange[Our Features]")
    features = st.columns(2)
    
    # Feature items in a visually appealing manner
    with features[0]:
        st.markdown('<div class="features">', unsafe_allow_html=True)
        st.write(" - :blue[**Object Detection**] - Real-time object detection with continuous audio feedback.")
        st.write(" - :blue[**Text to Speech**] - Convert visual data into audio for enhanced accessibility.")
        st.markdown('</div>', unsafe_allow_html=True)

    with features[1]:
        st.markdown('<div class="features">', unsafe_allow_html=True)
        st.write(" - :blue[**GPS Navigation**] - Seamless integration with GPS to guide users through environments.")
        st.write(" - :blue[**Speech Assistance**] - Communicate with your surroundings using voice recognition.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Additional Features Section
    st.write('<hr>', unsafe_allow_html=True)  # Horizontal line for separation
    st.subheader(":orange[More Features]")
    more_features = st.columns(3)

    # Additional Features
    with more_features[0]:
        st.markdown('<div class="features">', unsafe_allow_html=True)
        st.write(" - :blue[**Multi-Language Support**] - Real-time translation and support for multiple languages.")
        st.markdown('</div>', unsafe_allow_html=True)

    with more_features[1]:
        st.markdown('<div class="features">', unsafe_allow_html=True)
        st.write(" - :blue[**User-Friendly Interface**] - Simple and intuitive design for ease of use.")
        st.markdown('</div>', unsafe_allow_html=True)

    with more_features[2]:
        st.markdown('<div class="features">', unsafe_allow_html=True)
        st.write(" - :blue[**Customization Options**] - Personalize settings to match individual needs.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Call to Action
    st.write('<hr>', unsafe_allow_html=True)  # Another horizontal line for separation
    st.markdown("<h3>Get Started with Veritas View Today!</h3>", unsafe_allow_html=True)
    st.write("Join us in empowering the visually impaired community. [Contact us for more information](mailto:info@veritasview.com)!")
    
if __name__ == "__main__":
    app()
