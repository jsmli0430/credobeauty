import pandas as pd
import streamlit as st
import plotly.express as px
import re
import random

# Load data
@st.cache_resource
def load_data():
    # Load datasets
    df_credo = pd.read_csv('credo_finaldata.csv')
    df_sephora = pd.read_csv('sephoraproduct_info.csv')
    
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

elif page == "Product Showcase":
    st.title("Product Showcase")

    # 过滤选项
    st.sidebar.header("Filter Options")
    selected_skin_type = st.sidebar.multiselect(
        "Select Skin Type",
        options=["all skin", "dry skin", "oily skin", "sensitive skin", "normal skin", "combination skin","acne-prone skin","aging skin"],
        default=["all skin"]
    )
    selected_hair_type = st.sidebar.multiselect(
        "Select Hair Type",
        options=[
            "all hair", "damaged hair", "dry hair", "oily hair", 
            "curly hair", "fine hair", "straight hair"
        ],
        default=[]
    )

    price_max = int(df_credo['price'].max()) if not df_credo['price'].isnull().all() else 100
    price_range = st.sidebar.slider(
        "Price Range",
        0, 
        price_max, 
        (0, 100)
    )

    # 过滤数据基于价格
    filtered_df = df_credo[
        (df_credo['price'] >= price_range[0]) & 
        (df_credo['price'] <= price_range[1])
    ].copy()

    filtered_df = filtered_df.sample(frac=1, random_state=42)

    # 替换 NaN 值
    numeric_fields = ['price', 'rating', 'reviews', 'sentiment']
    for field in numeric_fields:
        if field in filtered_df.columns:
            filtered_df[field] = filtered_df[field].fillna(0)

    string_fields = ['suitable_type', 'ingredients', 'first_sentence']
    for field in string_fields:
        if field in filtered_df.columns:
            filtered_df[field] = filtered_df[field].fillna('')

    # 显示产品数量
    st.subheader(f"Products Matching Your Preferences ({len(filtered_df)} found)")

    # 定义一个函数来格式化适用肤质和成分
    def format_display(field_value):
        if field_value:
            # 移除方括号和引号
            clean_value = field_value.strip("[]").replace("'", "").replace('"', "")
            items = [item.strip() for item in clean_value.split(',') if item.strip()]
            return ", ".join([
                f'<span style="background-color:#e0e0e0; padding:2px 4px; border-radius:3px; margin-right:2px;">{item}</span>'
                for item in items
            ])
        return ""

    # 遍历每个产品并展示
    for _, row in filtered_df.iterrows():
        # 确保字段存在并处理 NaN
        brand_name = row.get('brand_name', 'Unknown Brand') or 'Unknown Brand'
        product_name = row.get('product_name', 'Unknown Product') or 'Unknown Product'
        price = row['price']
        rating = row['rating']
        reviews = int(row['reviews']) if row['reviews'] else 0
        suitable_type = row['suitable_type']
        ingredients = row['ingredients']
        sentiment = row['sentiment']
        first_sentence = row['first_sentence']
        image_url = row.get('image_url', 'https://via.placeholder.com/150')
        
        # 格式化适用肤质和成分显示
        suitable_display = f"<p><strong>Suitable for:</strong> {format_display(suitable_type)}</p>" if suitable_type else ""
        ingredients_display = f"<p><strong>Ingredients:</strong> {format_display(ingredients)}</p>" if ingredients else ""
        sentiment_display = f"<p><strong>Sentiment:</strong> {sentiment}</p>" if sentiment else "sentiment,"
        review_display = f"<p><strong>Review:</strong> {first_sentence}</p>" if first_sentence else "review summary x available."
        
        # 清理适用字段
        suitable_clean = suitable_type.strip("[]").replace("'", "").replace('"', "")
        product_types = [item.strip() for item in suitable_clean.split(',') if item.strip()]
    
        # 用户选择的所有条件
        selected_types = selected_skin_type + selected_hair_type
    
        # 推荐等级逻辑
        is_recommend = all(option in product_types for option in selected_types)
        is_good = any(option in product_types for option in selected_types) and not is_recommend
        is_maybe = not is_good and not is_recommend
    
        # 定义 CSS 样式和徽章
        if is_recommend:
            badge = '<span style="background-color:#a4d1b8; color:white; padding:2px 6px; border-radius:3px; font-size:12px;">Recommended for you</span>'
            container_style = "border:2px solid #a4d1b8; padding:10px; border-radius:5px; background-color:#f3fbf6;"
        elif is_good:
            badge = '<span style="background-color:#fec692; color:white; padding:2px 6px; border-radius:3px; font-size:12px;">Good Match</span>'
            container_style = "border:2px solid #fec692; padding:10px; border-radius:5px; background-color:#fff9f1;"
        else:  # is_maybe
            badge = '<span style="background-color:#d48ba3; color:white; padding:2px 6px; border-radius:3px; font-size:12px;">Maybe</span>'
            container_style = "border:2px solid #d48ba3; padding:10px; border-radius:5px; background-color:#fff8fa;"
    
        # 构建 HTML 内容
        html_content = f"""
            <div style="{container_style}">
                <div style="display: flex; align-items: center;">
                    <img src="{image_url}" width="150" style="border-radius:5px;">
                    <div style="margin-left:20px; flex: 1;">
                        <h3 style="margin:0;">{brand_name}: {product_name}</h3>
                        {badge}
                        <p><strong>Price:</strong> ${price}</p>
                        <p><strong>Rating:</strong> {rating} ({reviews} reviews)</p>
                        <p><strong>Brand:</strong> {brand_name}</p>
                        {suitable_display}
                        {ingredients_display}
                        {sentiment_display}
                        {review_display}
                    </div>
                </div>
            </div>
            <br/>
        """
    
        # 渲染 HTML 内容（确保所有情况都用 unsafe_allow_html）
        st.markdown(html_content, unsafe_allow_html=True)


