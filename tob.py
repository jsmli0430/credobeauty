import pandas as pd
import streamlit as st
import plotly.express as px
import re

# Load data
@st.cache_resource
def load_data():
    # Load datasets
    df_credo = pd.read_csv('data/credo_finaldata.csv')
    df_sephora = pd.read_csv('data/sephoraproduct_info.csv')
    
    # Clean and standardize columns for Credo
    df_credo.rename(columns={
        'id': 'product_id',
        'name': 'product_name',
        'price': 'price',
        'rating': 'rating',
        'review_count': 'reviews',
        'brand_name': 'brand_name'
    }, inplace=True)
    
    # Clean and standardize columns for Sephora
    df_sephora.rename(columns={
        'product_id': 'product_id',
        'product_name': 'product_name',
        'brand_name': 'brand_name',
        'price_usd': 'price',
        'rating': 'rating',
        'reviews': 'reviews'
    }, inplace=True)
    
    # Define price extraction function
    def extract_price(price_str):
        if pd.isnull(price_str):
            return None
        match = re.findall(r'[\d\.]+', str(price_str))
        if match:
            return float(match[0])
        else:
            return None
    
    # Apply price extraction
    df_credo['price'] = df_credo['price'].apply(extract_price)
    df_sephora['price'] = df_sephora['price'].apply(extract_price)
    
    # Drop rows with invalid prices
    df_credo = df_credo.dropna(subset=['price'])
    df_sephora = df_sephora.dropna(subset=['price'])
    
    # Convert ratings and reviews to numeric
    df_credo['rating'] = pd.to_numeric(df_credo['rating'], errors='coerce')
    df_sephora['rating'] = pd.to_numeric(df_sephora['rating'], errors='coerce')
    
    df_credo['reviews'] = pd.to_numeric(df_credo['reviews'], errors='coerce')
    df_sephora['reviews'] = pd.to_numeric(df_sephora['reviews'], errors='coerce')
    
    # Add source column
    df_credo['source'] = 'Credo'
    df_sephora['source'] = 'Sephora'
    
    # Combine datasets
    df_combined = pd.concat([df_credo, df_sephora], ignore_index=True)
    
    return df_credo, df_sephora, df_combined

# Load data
df_credo, df_sephora, df_combined = load_data()

# Sidebar for page selection
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a Page", ["Overview Metrics", "Product Showcase"])

### Overview Metrics Page
if page == "Overview Metrics":
    st.title("Credo Beauty vs. Sephora: Competitive Analysis")
    
    # Compute metrics
    num_brands_credo = df_credo['brand_name'].nunique()
    num_brands_sephora = df_sephora['brand_name'].nunique()
    
    num_products_credo = df_credo['product_id'].nunique()
    num_products_sephora = df_sephora['product_id'].nunique()
    
    avg_price_credo = df_credo['price'].mean()
    avg_price_sephora = df_sephora['price'].mean()
    
    median_price_credo = df_credo['price'].median()
    median_price_sephora = df_sephora['price'].median()
    
    avg_rating_credo = df_credo['rating'].mean()
    avg_rating_sephora = df_sephora['rating'].mean()
    
    median_rating_credo = df_credo['rating'].median()
    median_rating_sephora = df_sephora['rating'].median()
    
    avg_reviews_credo = df_credo['reviews'].mean()
    avg_reviews_sephora = df_sephora['reviews'].mean()
    
    price_min_credo = df_credo['price'].min()
    price_max_credo = df_credo['price'].max()
    
    price_min_sephora = df_sephora['price'].min()
    price_max_sephora = df_sephora['price'].max()
    
    # Overview Metrics
    st.header('Overview Metrics')
    
    # Create columns for Credo and Sephora
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div style="background-color:#d8e6f5; padding:15px; border-radius:10px;">
                <h4>Credo</h4>
                <p><strong>Number of Brands:</strong> {}</p>
                <p><strong>Number of Products:</strong> {}</p>
            </div>
            """.format(num_brands_credo, num_products_credo),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style="background-color:#f7d7d9; padding:15px; border-radius:10px;">
                <h4>Sephora</h4>
                <p><strong>Number of Brands:</strong> {}</p>
                <p><strong>Number of Products:</strong> {}</p>
            </div>
            """.format(num_brands_sephora, num_products_sephora),
            unsafe_allow_html=True
        )
    
    # Price Metrics
    st.subheader('Price Metrics')
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown(
            """
            <div style="background-color:#d8e6f5; padding:15px; border-radius:10px;">
                <h4>Credo</h4>
                <p><strong>Average Price:</strong> ${:.2f}</p>
                <p><strong>Median Price:</strong> ${:.2f}</p>
                <p><strong>Price Range:</strong> ${:.2f} - ${:.2f}</p>
            </div>
            """.format(avg_price_credo, median_price_credo, price_min_credo, price_max_credo),
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            """
            <div style="background-color:#f7d7d9; padding:15px; border-radius:10px;">
                <h4>Sephora</h4>
                <p><strong>Average Price:</strong> ${:.2f}</p>
                <p><strong>Median Price:</strong> ${:.2f}</p>
                <p><strong>Price Range:</strong> ${:.2f} - ${:.2f}</p>
            </div>
            """.format(avg_price_sephora, median_price_sephora, price_min_sephora, price_max_sephora),
            unsafe_allow_html=True
        )
    
    # Rating Metrics
    st.subheader('Rating Metrics')
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown(
            """
            <div style="background-color:#d8e6f5; padding:15px; border-radius:10px;">
                <h4>Credo</h4>
                <p><strong>Average Rating:</strong> {:.2f}</p>
                <p><strong>Median Rating:</strong> {:.2f}</p>
                <p><strong>Average Review Count:</strong> {:.0f}</p>
            </div>
            """.format(avg_rating_credo, median_rating_credo, avg_reviews_credo),
            unsafe_allow_html=True
        )
    
    with col6:
        st.markdown(
            """
            <div style="background-color:#f7d7d9; padding:15px; border-radius:10px;">
                <h4>Sephora</h4>
                <p><strong>Average Rating:</strong> {:.2f}</p>
                <p><strong>Median Rating:</strong> {:.2f}</p>
                <p><strong>Average Review Count:</strong> {:.0f}</p>
            </div>
            """.format(avg_rating_sephora, median_rating_sephora, avg_reviews_sephora),
            unsafe_allow_html=True
        )
    
    # Price Distribution
    st.header('Price Distribution by Price Range')
    
    price_bins = [0, 25, 50, 100, 200, df_combined['price'].max()]
    price_labels = ['Budget ($0-25)', 'Low Price ($25-50)', 'Mid Price ($50-100)', 'High Price ($100-200)', 'Luxury ($200+)']
    
    df_combined['price_bin'] = pd.cut(df_combined['price'], bins=price_bins, labels=price_labels, include_lowest=True)
    
    price_distribution = df_combined.groupby(['source', 'price_bin']).size().reset_index(name='count')
    total_counts = price_distribution.groupby('source')['count'].transform('sum')
    price_distribution['percent'] = price_distribution['count'] / total_counts * 100
    
    fig_price_bar = px.bar(
        price_distribution,
        x='price_bin',
        y='percent',
        color='source',
        color_discrete_map={'Credo': '#d8e6f5', 'Sephora': '#f7d7d9'},
        barmode='group',
        text=price_distribution['percent'].round(1),
        title='Price Distribution by Price Range',
        labels={'price_bin': 'Price Range', 'percent': 'Percentage (%)'}
    )
    fig_price_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_price_bar)
    
    # Rating Distribution
    st.header('Rating Distribution by Rating Range')
    
    rating_bins = [0, 2, 3, 4, 5]
    rating_labels = ['0-2', '2-3', '3-4', '4-5']
    
    df_combined['rating_bin'] = pd.cut(df_combined['rating'], bins=rating_bins, labels=rating_labels, include_lowest=True)
    
    rating_distribution = df_combined.groupby(['source', 'rating_bin']).size().reset_index(name='count')
    total_counts_rating = rating_distribution.groupby('source')['count'].transform('sum')
    rating_distribution['percent'] = rating_distribution['count'] / total_counts_rating * 100
    
    fig_rating_bar = px.bar(
        rating_distribution,
        x='rating_bin',
        y='percent',
        color='source',
        color_discrete_map={'Credo': '#d8e6f5', 'Sephora': '#f7d7d9'},
        barmode='group',
        text=rating_distribution['percent'].round(1),
        title='Rating Distribution by Rating Range',
        labels={'rating_bin': 'Rating Range', 'percent': 'Percentage (%)'}
    )
    fig_rating_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_rating_bar)
    
    # Box Plot: Rating vs Price Range
    st.header('Rating Distribution Across Price Ranges')
    
    fig_box = px.box(
        df_combined,
        x='price_bin',
        y='rating',
        color='source',
        color_discrete_map={'Credo': '#d8e6f5', 'Sephora': '#f7d7d9'},
        title='Rating Distribution Across Price Ranges',
        labels={'price_bin': 'Price Range', 'rating': 'Rating'}
    )
    st.plotly_chart(fig_box)
    
    # Brand Comparison
    st.header('Select a Brand to Compare')
    
    common_brands = set(df_credo['brand_name'].unique()).intersection(set(df_sephora['brand_name'].unique()))
    common_brands = sorted(list(common_brands))
    
    if common_brands:
        selected_brand = st.selectbox('Select a Brand', options=common_brands)
        
        # Filter data for selected brand
        df_brand = df_combined[df_combined['brand_name'] == selected_brand]
        
        # Split by source
        df_brand_credo = df_brand[df_brand['source'] == 'Credo']
        df_brand_sephora = df_brand[df_brand['source'] == 'Sephora']
        
        # Calculate metrics
        avg_price_brand_credo = df_brand_credo['price'].mean()
        avg_price_brand_sephora = df_brand_sephora['price'].mean()
        
        avg_rating_brand_credo = df_brand_credo['rating'].mean()
        avg_rating_brand_sephora = df_brand_sephora['rating'].mean()
        
        # Display metrics
        st.subheader(f'Average Price and Rating for {selected_brand}')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                """
                <div style="background-color:#d8e6f5; padding:15px; border-radius:10px;">
                    <h4>Credo</h4>
                    <p><strong>Average Price:</strong> ${:.2f}</p>
                    <p><strong>Average Rating:</strong> {:.2f}</p>
                </div>
                """.format(avg_price_brand_credo, avg_rating_brand_credo),
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                """
                <div style="background-color:#f7d7d9; padding:15px; border-radius:10px;">
                    <h4>Sephora</h4>
                    <p><strong>Average Price:</strong> ${:.2f}</p>
                    <p><strong>Average Rating:</strong> {:.2f}</p>
                </div>
                """.format(avg_price_brand_sephora, avg_rating_brand_sephora),
                unsafe_allow_html=True
            )
        
        # Price Distribution for selected brand
        st.subheader(f'Price Distribution for {selected_brand}')
        
        df_brand['price_bin'] = pd.cut(df_brand['price'], bins=price_bins, labels=price_labels, include_lowest=True)
        
        brand_price_distribution = df_brand.groupby(['source', 'price_bin']).size().reset_index(name='count')
        total_counts_brand_price = brand_price_distribution.groupby('source')['count'].transform('sum')
        brand_price_distribution['percent'] = brand_price_distribution['count'] / total_counts_brand_price * 100
        
        fig_brand_price_bar = px.bar(
            brand_price_distribution,
            x='price_bin',
            y='percent',
            color='source',
            color_discrete_map={'Credo': '#d8e6f5', 'Sephora': '#f7d7d9'},
            barmode='group',
            text=brand_price_distribution['percent'].round(1),
            title=f'Price Distribution for {selected_brand}',
            labels={'price_bin': 'Price Range', 'percent': 'Percentage (%)'}
        )
        fig_brand_price_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_brand_price_bar)
    else:
        st.write('No common brands between Credo and Sephora.')

### Product Showcase Page
elif page == "Product Showcase":
    st.title("Product Showcase")
    
    # Filter options
    st.sidebar.header("Filter Options")
    selected_skin_type = st.sidebar.multiselect(
        "Select Skin Type",
        options=["all skin", "dry skin", "oily skin", "sensitive skin", "normal skin", "combination skin"],
        default=[]
    )
    price_range = st.sidebar.slider(
        "Price Range",
        0, 
        int(df_credo['price'].max()), 
        (0, 100)
    )
    
    # Filter data based on price
    filtered_df = df_credo[
        (df_credo['price'] >= price_range[0]) & 
        (df_credo['price'] <= price_range[1])
    ]
    
    # Show number of products
    st.subheader(f"Products Matching Your Preferences ({len(filtered_df)} found)")
    
    for _, row in filtered_df.iterrows():
        # Check if recommended
        is_recommended = False
        if selected_skin_type:
            product_skin_types = row['suitable_ type'].split(',') if isinstance(row['suitable_type'], str) else []
            is_recommended = any(skin in product_skin_types for skin in selected_skin_type)
        
        # Define CSS style based on recommendation
        if is_recommended:
            st.markdown(
                f"""
                <div style="border:2px solid #4CAF50; padding:10px; border-radius:5px; background-color:#f9fff9;">
                    <div style="display: flex; align-items: center;">
                        <img src="https://via.placeholder.com/150" width="150" style="border-radius:5px;">
                        <div style="margin-left:20px;">
                            <h3 style="margin:0;">{row['brand_name']}: {row['product_name']}</h3>
                            <span style="background-color:#4CAF50; color:white; padding:2px 6px; border-radius:3px; font-size:12px;">Recommended for you</span>
                            <p><strong>Price:</strong> ${row['price']}</p>
                            <p><strong>Rating:</strong> {row['rating']} ({row['reviews']} reviews)</p>
                            <p><strong>Brand:</strong> {row['brand_name']}</p>
                            {"<p><strong>Suitable for:</strong> " + ", ".join([f"<span style='background-color:#e0e0e0; padding:2px 4px; border-radius:3px; margin-right:2px;'>{skin.strip()}</span>" for skin in row['suitable_type'].split(',')]) + "</p>" if row.get('suitable_type') else ""}
                            {"<p><strong>Ingredients:</strong> " + ", ".join([f"<span style='background-color:#e0e0e0; padding:2px 4px; border-radius:3px; margin-right:2px;'>{ing.strip()}</span>" for ing in row['ingredients'].split(',')]) + "</p>" if row.get('ingredients') else ""}
                            {"<p><strong>Sentiment:</strong> " + row['sentiment'] + "</p>" if row.get('sentiment') else ""}
                            {"<p><strong>Review:</strong> " + row['first_sentence'] + "</p>" if row.get('first_sentence') else ""}
                        </div>
                    </div>
                </div>
                <br/>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="border:1px solid #ccc; padding:10px; border-radius:5px;">
                    <div style="display: flex; align-items: center;">
                        <img src="https://via.placeholder.com/150" width="150" style="border-radius:5px;">
                        <div style="margin-left:20px;">
                            <h3 style="margin:0;">{row['brand_name']}: {row['product_name']}</h3>
                            <p><strong>Price:</strong> ${row['price']}</p>
                            <p><strong>Rating:</strong> {row['rating']} ({row['reviews']} reviews)</p>
                            <p><strong>Brand:</strong> {row['brand_name']}</p>
                            {"<p><strong>Suitable for:</strong> " + ", ".join([f"<span style='background-color:#e0e0e0; padding:2px 4px; border-radius:3px; margin-right:2px;'>{skin.strip()}</span>" for skin in row['suitable_type'].split(',')]) + "</p>" if row.get('suitable_type') else ""}
                            {"<p><strong>Ingredients:</strong> " + ", ".join([f"<span style='background-color:#e0e0e0; padding:2px 4px; border-radius:3px; margin-right:2px;'>{ing.strip()}</span>" for ing in row['ingredients'].split(',')]) + "</p>" if row.get('ingredients') else ""}
                            {"<p><strong>Sentiment:</strong> " + row['sentiment'] + "</p>" if row.get('sentiment') else ""}
                            {"<p><strong>Review:</strong> " + row['first_sentence'] + "</p>" if row.get('first_sentence') else ""}
                        </div>
                    </div>
                </div>
                <br/>
                """,
                unsafe_allow_html=True
            )
