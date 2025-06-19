import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json

# Page Configuration
st.set_page_config(
    page_title="ZipLink - URL Management Platform",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Light Theme Color Palette - Professional Light Theme
COLORS = {
    'primary': '#2E86AB',  # Professional Blue
    'secondary': '#A23B72',  # Accent Purple
    'success': '#28A745',  # Success Green
    'warning': '#FFC107',  # Warning Yellow
    'danger': '#DC3545',  # Error Red
    'light': '#FFFFFF',  # Light Background
    'lighter': '#F8F9FA',  # Lighter Background
    'dark': '#212529',  # Dark Text
    'muted': '#6C757D',  # Muted Text
    'border': '#DEE2E6',  # Border Color
    'card': '#FFFFFF',  # Card Background
    'input': '#FFFFFF',  # Input Background
    'sidebar': '#F1F3F4'  # Sidebar Background
}


# Custom CSS Styling - Light Theme
def load_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Ubuntu:wght@300;400;500;700&display=swap');

    /* Global Styles */
    .stApp {{
        background-color: {COLORS['light']};
        font-family: 'Ubuntu', sans-serif;
        color: {COLORS['dark']};
    }}

    /* Sidebar Styling */
    .css-1d391kg {{
        background-color: {COLORS['sidebar']};
        border-right: 1px solid {COLORS['border']};
    }}

    /* Main Content */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        background-color: {COLORS['light']};
    }}

    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Ubuntu', sans-serif;
        color: {COLORS['dark']};
        font-weight: 500;
    }}

    /* Custom Components */
    .metric-card {{
        background: {COLORS['card']};
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid {COLORS['border']};
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}

    .info-card {{
        background: {COLORS['card']};
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 4px solid {COLORS['primary']};
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}

    .url-item {{
        background: {COLORS['card']};
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid {COLORS['border']};
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}

    .success-alert {{
        background: rgba(40, 167, 69, 0.1);
        border: 1px solid {COLORS['success']};
        color: {COLORS['success']};
        padding: 0.75rem;
        border-radius: 6px;
        margin: 1rem 0;
    }}

    .error-alert {{
        background: rgba(220, 53, 69, 0.1);
        border: 1px solid {COLORS['danger']};
        color: {COLORS['danger']};
        padding: 0.75rem;
        border-radius: 6px;
        margin: 1rem 0;
    }}

    /* Button Styling */
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-family: 'Ubuntu', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
    }}

    .stButton > button:hover {{
        background-color: #1e5f82;
        box-shadow: 0 2px 8px rgba(46, 134, 171, 0.3);
    }}

    /* Form Styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {{
        background-color: {COLORS['input']};
        border: 1px solid {COLORS['border']};
        color: {COLORS['dark']};
        border-radius: 6px;
    }}

    /* User Info Card */
    .user-info {{
        background: {COLORS['card']};
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid {COLORS['border']};
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}

    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem 0;
        color: {COLORS['muted']};
        border-top: 1px solid {COLORS['border']};
        margin-top: 3rem;
        background-color: {COLORS['lighter']};
    }}

    /* Hyperlink Styling */
    .url-link {{
        color: {COLORS['primary']};
        text-decoration: none;
        word-break: break-all;
        transition: color 0.3s ease;
    }}

    .url-link:hover {{
        color: {COLORS['secondary']};
        text-decoration: underline;
    }}

    /* Admin Panel Styling */
    .admin-user-card {{
        background: {COLORS['card']};
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid {COLORS['border']};
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}

    .danger-button {{
        background-color: {COLORS['danger']} !important;
        color: white !important;
    }}

    .danger-button:hover {{
        background-color: #c82333 !important;
    }}

    /* Hide Streamlit Elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Plotly Chart Styling */
    .js-plotly-plot .plotly .modebar {{
        background-color: {COLORS['card']};
    }}
    </style>
    """, unsafe_allow_html=True)


# API Configuration
API_BASE_URL = "http://localhost:8000"


# Initialize Session State
def init_session_state():
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
    if 'confirm_delete_user' not in st.session_state:
        st.session_state.confirm_delete_user = None
    if 'confirm_delete_url' not in st.session_state:
        st.session_state.confirm_delete_url = None


# API Helper Functions
def make_api_request(endpoint, method='GET', data=None, auth_required=True):
    """Make API request with proper error handling"""
    try:
        headers = {'Content-Type': 'application/json'}
        if auth_required and st.session_state.access_token:
            headers['Authorization'] = f"Bearer {st.session_state.access_token}"

        url = f"{API_BASE_URL}{endpoint}"

        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)

        return response
    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Connection Error: Cannot connect to the backend server. Please ensure the FastAPI server is running on http://localhost:8000")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request Timeout: The server is taking too long to respond.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"🚫 Request Error: {str(e)}")
        return None


# Authentication Functions
def login_user(username, password):
    """Authenticate user and get JWT token"""
    data = {
        'username': username,
        'password': password
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/token",
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )

        if response.status_code == 200:
            token_data = response.json()
            st.session_state.access_token = token_data['access_token']

            # Get user info
            user_response = make_api_request('/users/')
            if user_response and user_response.status_code == 200:
                st.session_state.user_info = user_response.json()
                st.session_state.authentication_status = True
                return True
            else:
                st.error("Failed to fetch user information")
                return False
        else:
            error_detail = response.json().get('detail', 'Authentication failed')
            st.error(f"Login failed: {error_detail}")
            return False

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Connection Error: Cannot connect to the backend server. Please ensure the FastAPI server is running.")
        return False
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False


def register_user(email, username, firstname, lastname, password, role='user'):
    """Register new user"""
    data = {
        'email': email,
        'username': username,
        'firstname': firstname,
        'lastname': lastname,
        'password': password,
        'role': role
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/",
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 201:
            return True
        else:
            error_detail = response.json().get('detail', 'Registration failed')
            st.error(f"Registration failed: {error_detail}")
            return False

    except requests.exceptions.ConnectionError:
        st.error("❌ Connection Error: Cannot connect to the backend server.")
        return False
    except Exception as e:
        st.error(f"Registration error: {str(e)}")
        return False


def logout_user():
    """Logout user and clear session"""
    st.session_state.authentication_status = False
    st.session_state.user_info = None
    st.session_state.access_token = None
    st.session_state.current_page = 'Dashboard'
    st.session_state.confirm_delete_user = None
    st.session_state.confirm_delete_url = None


# UI Components
def render_success_alert(message):
    """Render success alert"""
    st.markdown(f"""
    <div class="success-alert">
        <strong>✅ Success:</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def render_error_alert(message):
    """Render error alert"""
    st.markdown(f"""
    <div class="error-alert">
        <strong>❌ Error:</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(title, value, delta=None, delta_color="normal"):
    """Render metric card component"""
    delta_html = ""
    if delta:
        color = COLORS['success'] if delta_color == "normal" else COLORS['danger']
        delta_html = f'<p style="color: {color}; font-size: 0.9rem; margin: 0;">{delta}</p>'

    st.markdown(f"""
    <div class="metric-card">
        <h4 style="margin: 0; color: {COLORS['muted']}; font-size: 0.9rem; font-weight: 400;">{title}</h4>
        <h2 style="margin: 0.5rem 0 0 0; color: {COLORS['dark']}; font-weight: 700;">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_info_card(title, content):
    """Render info card component"""
    st.markdown(f"""
    <div class="info-card">
        <h4 style="margin: 0 0 0.5rem 0; color: {COLORS['dark']};">{title}</h4>
        <p style="margin: 0; color: {COLORS['muted']};">{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_url_item(url_data):
    """Render URL item component with correct short URL format"""
    # Correct format: /urls/{short_code} for redirection
    short_url = f"{API_BASE_URL}/urls/{url_data.get('short_code', '')}"
    long_url = url_data.get('url', 'N/A')
    created_date = url_data.get('created_at', '')

    if created_date:
        try:
            if isinstance(created_date, str):
                created_date = datetime.fromisoformat(created_date.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
            else:
                created_date = created_date.strftime('%Y-%m-%d %H:%M')
        except:
            created_date = 'N/A'

    st.markdown(f"""
    <div class="url-item">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
            <h4 style="margin: 0; color: {COLORS['dark']};">{url_data.get('short_code', 'N/A')}</h4>
            <span style="color: {COLORS['muted']}; font-size: 0.8rem;">{created_date}</span>
        </div>
        <p style="margin: 0.5rem 0;">
            <a href="{short_url}" target="_blank" class="url-link">{short_url}</a>
        </p>
        <p style="margin: 0.5rem 0;">
            <a href="{long_url}" target="_blank" class="url-link">{long_url}</a>
        </p>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
            <span style="color: {COLORS['success']}; font-size: 0.9rem;">Clicks: {url_data.get('access_count', 0)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_admin_user_card(user_data):
    """Render admin user card component"""
    st.markdown(f"""
    <div class="admin-user-card">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
            <div>
                <h4 style="margin: 0; color: {COLORS['dark']};">{user_data.get('firstname', '')} {user_data.get('lastname', '')}</h4>
                <p style="margin: 0.25rem 0; color: {COLORS['muted']};">@{user_data.get('username', '')} • {user_data.get('email', '')}</p>
                <p style="margin: 0; color: {COLORS['primary']}; font-size: 0.9rem; text-transform: capitalize;">Role: {user_data.get('role', 'user')}</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0; color: {COLORS['muted']}; font-size: 0.8rem;">ID: {user_data.get('id', 'N/A')}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_admin_url_card(url_data):
    """Render admin URL card component with correct short URL format"""
    # Correct format: /urls/{short_code} for redirection
    short_url = f"{API_BASE_URL}/urls/{url_data.get('short_code', '')}"
    long_url = url_data.get('url', 'N/A')
    owner_id = url_data.get('owner_id', 'N/A')
    created_date = url_data.get('created_at', '')

    if created_date:
        try:
            if isinstance(created_date, str):
                created_date = datetime.fromisoformat(created_date.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
            else:
                created_date = created_date.strftime('%Y-%m-%d %H:%M')
        except:
            created_date = 'N/A'

    st.markdown(f"""
    <div class="admin-user-card">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
            <div>
                <h4 style="margin: 0; color: {COLORS['dark']};">{url_data.get('short_code', 'N/A')}</h4>
                <p style="margin: 0.25rem 0;">
                    <a href="{short_url}" target="_blank" class="url-link">{short_url}</a>
                </p>
                <p style="margin: 0.25rem 0;">
                    <a href="{long_url}" target="_blank" class="url-link">{long_url}</a>
                </p>
                <p style="margin: 0; color: {COLORS['muted']}; font-size: 0.9rem;">Owner ID: {owner_id} • Clicks: {url_data.get('access_count', 0)}</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0; color: {COLORS['muted']}; font-size: 0.8rem;">{created_date}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Authentication Page
def render_auth_page():
    """Render authentication page"""
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: {COLORS['primary']}; font-size: 3rem; margin-bottom: 0.5rem;">🔗 ZipLink</h1>
        <h3 style="color: {COLORS['muted']}; font-weight: 300; margin-bottom: 2rem;">Professional URL Management Platform</h3>
    </div>
    """, unsafe_allow_html=True)

    # Check backend connection
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
        if response.status_code != 200:
            st.warning("⚠️ Backend server might not be running properly. Please check the FastAPI server.")
    except:
        st.error("❌ Cannot connect to backend server. Please ensure FastAPI is running on http://localhost:8000")
        st.info("💡 To start the backend server, run: `uvicorn main:app --reload`")

    # Authentication tabs
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.markdown("### Authentication")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_login = st.form_submit_button("Login", use_container_width=True)

            if submit_login:
                if username and password:
                    with st.spinner("Authenticating..."):
                        if login_user(username, password):
                            render_success_alert("Login successful! Redirecting...")
                            st.rerun()
                else:
                    render_error_alert("Please fill in all fields.")

    with tab2:
        st.markdown("### Create Account")
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                firstname = st.text_input("First Name", placeholder="Enter first name")
                username = st.text_input("Username", placeholder="Choose username")
            with col2:
                lastname = st.text_input("Last Name", placeholder="Enter last name")
                email = st.text_input("Email", placeholder="Enter email address")

            password = st.text_input("Password", type="password", placeholder="Create password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            submit_register = st.form_submit_button("Create Account", use_container_width=True)

            if submit_register:
                if all([firstname, lastname, username, email, password, confirm_password]):
                    if password == confirm_password:
                        with st.spinner("Creating account..."):
                            if register_user(email, username, firstname, lastname, password):
                                render_success_alert("Account created successfully! Please login.")
                    else:
                        render_error_alert("Passwords do not match.")
                else:
                    render_error_alert("Please fill in all fields.")

    # Footer
    st.markdown(f"""
    <div class="footer">
        <p>© 2024 ZipLink - Professional URL Management Platform</p>
        <p style="margin-top: 0.5rem;">
            <a href="https://github.com/kxshrx/url-shortener" style="color: {COLORS['primary']}; text-decoration: none;">GitHub Repository</a> | 
            <a href="https://fastapi.tiangolo.com/" style="color: {COLORS['primary']}; text-decoration: none;">FastAPI Docs</a> | 
            <a href="mailto:support@ziplink.com" style="color: {COLORS['primary']}; text-decoration: none;">Support</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


# Sidebar Navigation
def render_sidebar():
    """Render sidebar with navigation"""
    with st.sidebar:
        # User Info
        if st.session_state.user_info:
            user = st.session_state.user_info
            st.markdown(f"""
            <div class="user-info">
                <h4 style="margin: 0 0 0.5rem 0; color: {COLORS['dark']};">{user.get('firstname', '')} {user.get('lastname', '')}</h4>
                <p style="margin: 0; color: {COLORS['muted']}; font-size: 0.9rem;">@{user.get('username', '')}</p>
                <p style="margin: 0.25rem 0 0 0; color: {COLORS['primary']}; font-size: 0.8rem; text-transform: capitalize;">{user.get('role', 'User')}</p>
            </div>
            """, unsafe_allow_html=True)

        # Navigation
        st.markdown("### Navigation")

        pages = ['Dashboard', 'URL Management', 'Analytics', 'Account Settings']
        if st.session_state.user_info and st.session_state.user_info.get('role') == 'admin':
            pages.append('System Administration')

        for page in pages:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()

        st.markdown("---")

        # Logout
        if st.button("Logout", use_container_width=True, type="secondary"):
            logout_user()
            st.rerun()

        # Quick Links
        st.markdown("### Quick Access")
        st.markdown(f"""
        <div style="margin-top: 1rem;">
            <p style="color: {COLORS['muted']}; font-size: 0.9rem; margin-bottom: 0.5rem;">Resources:</p>
            <a href="http://localhost:8000/docs" style="color: {COLORS['primary']}; text-decoration: none; font-size: 0.9rem;">📚 API Documentation</a><br>
            <a href="https://github.com/kxshrx/url-shortener" style="color: {COLORS['primary']}; text-decoration: none; font-size: 0.9rem;">🔧 GitHub Repository</a><br>
            <a href="mailto:support@ziplink.com" style="color: {COLORS['primary']}; text-decoration: none; font-size: 0.9rem;">💬 Support</a>
        </div>
        """, unsafe_allow_html=True)


# Dashboard Page - Without Quick Actions Section
def render_dashboard():
    """Render dashboard page without quick actions section"""
    st.markdown("# Dashboard")
    st.markdown("Welcome to your URL management dashboard")

    # Get user URLs for metrics
    response = make_api_request('/urls/')
    urls_count = 0
    total_clicks = 0
    active_urls = 0

    if response and response.status_code == 200:
        urls = response.json()
        urls_count = len(urls)
        total_clicks = sum(url.get('access_count', 0) for url in urls)
        active_urls = len([url for url in urls if url.get('access_count', 0) > 0])

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card("Total URLs", str(urls_count), f"+{urls_count} created", "normal")

    with col2:
        render_metric_card("Total Clicks", str(total_clicks), f"{total_clicks} total", "normal")

    with col3:
        render_metric_card("Active URLs", str(active_urls), f"{active_urls} with clicks", "normal")

    with col4:
        avg_ctr = f"{(total_clicks / urls_count * 100):.1f}%" if urls_count > 0 else "0%"
        render_metric_card("Avg. Clicks", avg_ctr, "per URL", "normal")

    # Recent Activity
    st.markdown("## Recent Activity")

    if response and response.status_code == 200 and urls:
        # Show recent URLs
        recent_urls = sorted(urls, key=lambda x: x.get('created_at', ''), reverse=True)[:5]
        for url_data in recent_urls:
            render_url_item(url_data)
    else:
        render_info_card("No URLs Found",
                         "You haven't created any short URLs yet. Go to URL Management to create your first one!")


# URL Management Page
def render_url_management():
    """Render URL management page"""
    st.markdown("# URL Management")
    st.markdown("Create, edit, and manage your short URLs")

    # Create new URL
    st.markdown("## Create Short URL")
    with st.form("create_url_form"):
        long_url = st.text_input("Long URL", placeholder="https://example.com/very-long-url")
        col1, col2 = st.columns([3, 1])
        with col2:
            submit_url = st.form_submit_button("Shorten URL", use_container_width=True)

        if submit_url and long_url:
            if not long_url.startswith(('http://', 'https://')):
                render_error_alert("Please enter a valid URL starting with http:// or https://")
            else:
                # API call to create short URL
                data = {'long_url': long_url}
                response = make_api_request('/urls/', method='POST', data=data)

                if response and response.status_code == 201:
                    url_data = response.json()
                    short_url = f"{API_BASE_URL}/urls/{url_data['short_code']}"
                    render_success_alert(f"Short URL created: {short_url}")
                    st.rerun()
                elif response:
                    error_detail = response.json().get('detail', 'Failed to create short URL')
                    render_error_alert(f"Failed to create short URL: {error_detail}")
                else:
                    render_error_alert("Failed to create short URL. Please check your connection.")

    # URL List
    st.markdown("## Your URLs")

    # Get user URLs
    response = make_api_request('/urls/')
    if response and response.status_code == 200:
        urls = response.json()

        if urls:
            for url_data in urls:
                col1, col2 = st.columns([4, 1])
                with col1:
                    render_url_item(url_data)
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Delete", key=f"del_{url_data['short_code']}", type="secondary"):
                        # Delete URL
                        del_response = make_api_request(f"/urls/{url_data['short_code']}", method='DELETE')
                        if del_response and del_response.status_code == 200:
                            render_success_alert("URL deleted successfully")
                            st.rerun()
                        else:
                            render_error_alert("Failed to delete URL")
        else:
            render_info_card("No URLs Found", "You haven't created any short URLs yet. Create your first one above!")
    elif response and response.status_code == 401:
        render_error_alert("Authentication expired. Please login again.")
        logout_user()
        st.rerun()
    else:
        render_error_alert("Failed to fetch URLs. Please check your connection.")


# Analytics Page
def render_analytics():
    """Render analytics page"""
    st.markdown("# Analytics")
    st.markdown("Detailed insights into your URL performance")

    # Get user URLs for analytics
    response = make_api_request('/urls/')
    if response and response.status_code == 200:
        urls = response.json()

        if urls:
            # Create analytics data
            df_urls = pd.DataFrame(urls)

            # Top URLs chart
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("## Top Performing URLs")
                top_urls = df_urls.nlargest(5, 'access_count')[['short_code', 'access_count']]
                if not top_urls.empty and top_urls['access_count'].sum() > 0:
                    fig = px.bar(
                        top_urls,
                        x='access_count',
                        y='short_code',
                        orientation='h',
                        title='Top URLs by Clicks'
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color=COLORS['dark']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No click data available yet.")

            with col2:
                st.markdown("## URL Statistics")
                total_urls = len(urls)
                total_clicks = df_urls['access_count'].sum()
                active_urls = len(df_urls[df_urls['access_count'] > 0])

                render_metric_card("Total URLs", str(total_urls))
                render_metric_card("Total Clicks", str(total_clicks))
                render_metric_card("Active URLs", str(active_urls))
        else:
            render_info_card("No Data Available", "Create some URLs first to see analytics.")
    else:
        render_error_alert("Failed to fetch analytics data.")


# Account Settings Page
def render_account_settings():
    """Render account settings page"""
    st.markdown("# Account Settings")
    st.markdown("Manage your account preferences and security")

    if st.session_state.user_info:
        user = st.session_state.user_info

        # Profile Information
        st.markdown("## Profile Information")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("First Name", value=user.get('firstname', ''), disabled=True)
            st.text_input("Username", value=user.get('username', ''), disabled=True)
        with col2:
            st.text_input("Last Name", value=user.get('lastname', ''), disabled=True)
            st.text_input("Role", value=user.get('role', '').title(), disabled=True)

        st.info("Profile editing will be available in a future update.")

        # Change Password
        st.markdown("## Change Password")
        with st.form("password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")

            change_password = st.form_submit_button("Change Password")

            if change_password:
                if all([current_password, new_password, confirm_password]):
                    if new_password == confirm_password:
                        if len(new_password) >= 6:
                            # API call to change password
                            data = {
                                'password': current_password,
                                'new_password': new_password
                            }
                            response = make_api_request('/users/password', method='PUT', data=data)

                            if response and response.status_code == 200:
                                render_success_alert("Password changed successfully!")
                            elif response and response.status_code == 403:
                                render_error_alert("Current password is incorrect.")
                            else:
                                render_error_alert("Failed to change password. Please try again.")
                        else:
                            render_error_alert("New password must be at least 6 characters long.")
                    else:
                        render_error_alert("New passwords do not match.")
                else:
                    render_error_alert("Please fill in all password fields.")


# System Administration Page - Fixed Admin Deletion with Backend Typo Fix
def render_admin_panel():
    """Render admin panel page with working deletion functionality"""
    if not st.session_state.user_info or st.session_state.user_info.get('role') != 'admin':
        render_error_alert("Access denied. Administrator privileges required.")
        return

    st.markdown("# System Administration")
    st.markdown("Manage users and system settings")

    # Get admin data using all 4 endpoints
    users_response = make_api_request('/admin/users')
    urls_response = make_api_request('/admin/urls')

    # System Metrics
    st.markdown("## System Overview")
    col1, col2, col3, col4 = st.columns(4)

    total_users = 0
    total_urls = 0

    if users_response and users_response.status_code == 200:
        total_users = len(users_response.json())

    if urls_response and urls_response.status_code == 200:
        total_urls = len(urls_response.json())

    with col1:
        render_metric_card("Total Users", str(total_users))

    with col2:
        render_metric_card("Total URLs", str(total_urls))

    with col3:
        render_metric_card("System Status", "Online", "All systems operational")

    with col4:
        render_metric_card("API Version", "v1.0", "Latest")

    # Tabs for different admin functions
    tab1, tab2 = st.tabs(["User Management", "URL Management"])

    with tab1:
        st.markdown("## User Management")

        if users_response and users_response.status_code == 200:
            users = users_response.json()

            if users:
                for user in users:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        render_admin_user_card(user)
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        user_id = user.get('id')
                        username = user.get('username')

                        # Check if this user is in confirmation state
                        if st.session_state.confirm_delete_user == user_id:
                            st.warning(f"⚠️ Confirm deletion of {username}")
                            col_confirm, col_cancel = st.columns(2)
                            with col_confirm:
                                if st.button("✅ Confirm", key=f"confirm_del_user_{user_id}", type="primary"):
                                    # Delete user using admin endpoint
                                    del_response = make_api_request(f"/admin/users/{user_id}", method='DELETE')
                                    if del_response and del_response.status_code == 200:
                                        render_success_alert(f"User {username} deleted successfully")
                                        st.session_state.confirm_delete_user = None
                                        st.rerun()
                                    else:
                                        render_error_alert(f"Failed to delete user {username}")
                                        st.session_state.confirm_delete_user = None
                            with col_cancel:
                                if st.button("❌ Cancel", key=f"cancel_del_user_{user_id}"):
                                    st.session_state.confirm_delete_user = None
                                    st.rerun()
                        else:
                            if st.button("🗑️ Delete", key=f"delete_user_{user_id}", type="secondary"):
                                st.session_state.confirm_delete_user = user_id
                                st.rerun()
            else:
                render_info_card("No Users", "No users found in the system.")
        else:
            render_error_alert("Failed to fetch user data.")

    with tab2:
        st.markdown("## URL Management")

        if urls_response and urls_response.status_code == 200:
            urls = urls_response.json()

            if urls:
                for url in urls:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        render_admin_url_card(url)
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        short_code = url.get('short_code')

                        # Check if this URL is in confirmation state
                        if st.session_state.confirm_delete_url == short_code:
                            st.warning(f"⚠️ Confirm deletion of {short_code}")
                            col_confirm, col_cancel = st.columns(2)
                            with col_confirm:
                                if st.button("✅ Confirm", key=f"confirm_del_url_{short_code}", type="primary"):
                                    # Delete URL using admin endpoint - FIXED: Use correct endpoint
                                    # Your backend has typo '/ur;s/' but we use the corrected '/urls/'
                                    del_response = make_api_request(f"/admin/urls/{short_code}", method='DELETE')
                                    if del_response and del_response.status_code == 200:
                                        render_success_alert(f"URL {short_code} deleted successfully")
                                        st.session_state.confirm_delete_url = None
                                        st.rerun()
                                    else:
                                        render_error_alert(f"Failed to delete URL {short_code}")
                                        st.session_state.confirm_delete_url = None
                            with col_cancel:
                                if st.button("❌ Cancel", key=f"cancel_del_url_{short_code}"):
                                    st.session_state.confirm_delete_url = None
                                    st.rerun()
                        else:
                            if st.button("🗑️ Delete", key=f"delete_url_{short_code}", type="secondary"):
                                st.session_state.confirm_delete_url = short_code
                                st.rerun()
            else:
                render_info_card("No URLs", "No URLs found in the system.")
        else:
            render_error_alert("Failed to fetch URL data.")


# Main Application
def main():
    """Main application function"""
    load_css()
    init_session_state()

    if not st.session_state.authentication_status:
        render_auth_page()
    else:
        render_sidebar()

        # Main content based on current page
        if st.session_state.current_page == 'Dashboard':
            render_dashboard()
        elif st.session_state.current_page == 'URL Management':
            render_url_management()
        elif st.session_state.current_page == 'Analytics':
            render_analytics()
        elif st.session_state.current_page == 'Account Settings':
            render_account_settings()
        elif st.session_state.current_page == 'System Administration':
            render_admin_panel()


if __name__ == "__main__":
    main()
