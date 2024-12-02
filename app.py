import pandas as pd
import streamlit as st
import plotly.express as px
import re

st.title('Credo Beauty v. Sephora Competitive Analysis')

# 加载数据
@st.cache_data
def load_data():
    # 从CSV文件加载数据
    df_credo = pd.read_csv('data/credoproduct_info.csv')
    df_sephora = pd.read_csv('data/sephoraproduct_info.csv')

    # 标准化列名
    df_credo.rename(columns={
        'id': 'product_id',
        'name': 'product_name',
        'brand_name': 'brand_name',
        'price': 'price',
        'rating': 'rating',
        'review_count': 'reviews'
    }, inplace=True)

    df_sephora.rename(columns={
        'product_id': 'product_id',
        'product_name': 'product_name',
        'brand_name': 'brand_name',
        'price_usd': 'price',
        'rating': 'rating',
        'reviews': 'reviews'
    }, inplace=True)

    # 处理价格数据，如"from $23"
    def extract_price(price_str):
        if pd.isnull(price_str):
            return None
        match = re.findall(r'[\d\.]+', str(price_str))
        if match:
            return float(match[0])
        else:
            return None

    # 应用价格提取函数
    df_credo['price'] = df_credo['price'].apply(extract_price)
    df_sephora['price'] = df_sephora['price'].apply(extract_price)

    # 删除无法转换价格的行
    df_credo = df_credo.dropna(subset=['price'])
    df_sephora = df_sephora.dropna(subset=['price'])

    # 转换评分列为数值型
    df_credo['rating'] = pd.to_numeric(df_credo['rating'], errors='coerce')
    df_sephora['rating'] = pd.to_numeric(df_sephora['rating'], errors='coerce')

    # 转换评论数为数值型
    df_credo['reviews'] = pd.to_numeric(df_credo['reviews'], errors='coerce')
    df_sephora['reviews'] = pd.to_numeric(df_sephora['reviews'], errors='coerce')

    # 添加来源列
    df_credo['source'] = 'Credo'
    df_sephora['source'] = 'Sephora'

    # 合并数据集
    df_combined = pd.concat([df_credo, df_sephora], ignore_index=True)

    return df_credo, df_sephora, df_combined

df_credo, df_sephora, df_combined = load_data()

# 计算额外的指标
# 品牌和产品数量
num_brands_credo = df_credo['brand_name'].nunique()
num_brands_sephora = df_sephora['brand_name'].nunique()

num_products_credo = df_credo['product_id'].nunique()
num_products_sephora = df_sephora['product_id'].nunique()

# 平均价格
avg_price_credo = df_credo['price'].mean()
avg_price_sephora = df_sephora['price'].mean()

# 中位数价格
median_price_credo = df_credo['price'].median()
median_price_sephora = df_sephora['price'].median()

# 平均评分
avg_rating_credo = df_credo['rating'].mean()
avg_rating_sephora = df_sephora['rating'].mean()

# 中位数评分
median_rating_credo = df_credo['rating'].median()
median_rating_sephora = df_sephora['rating'].median()

# 平均评论数
avg_reviews_credo = df_credo['reviews'].mean()
avg_reviews_sephora = df_sephora['reviews'].mean()

# 价格范围
price_min_credo = df_credo['price'].min()
price_max_credo = df_credo['price'].max()

price_min_sephora = df_sephora['price'].min()
price_max_sephora = df_sephora['price'].max()

# 概览指标
st.header('Overview Metrics')

# 创建并排的列
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div style="background-color:#d8e6f5; padding:15px; border-radius:10px;">', unsafe_allow_html=True)
    st.markdown('#### Credo', unsafe_allow_html=True)
    st.metric(label='Number of Brands', value=num_brands_credo)
    st.metric(label='Number of Products', value=num_products_credo)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="background-color:#f7d7d9; padding:15px; border-radius:10px;">', unsafe_allow_html=True)
    st.markdown('#### Sephora', unsafe_allow_html=True)
    st.metric(label='Number of Brands', value=num_brands_sephora)
    st.metric(label='Number of Products', value=num_products_sephora)
    st.markdown('</div>', unsafe_allow_html=True)

# 对其他部分也应用类似的样式
st.subheader('Price Metrics')

col3, col4 = st.columns(2)

with col3:
    st.markdown('<div style="background-color:#d8e6f5; padding:15px; border-radius:10px;">', unsafe_allow_html=True)
    st.markdown('#### Credo', unsafe_allow_html=True)
    st.metric(label='Average Price', value=f"${avg_price_credo:.0f}")
    st.metric(label='Median Price', value=f"${median_price_credo:.0f}")
    st.metric(label='Price Range', value=f"${price_min_credo:.0f} - ${price_max_credo:.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div style="background-color:#f7d7d9; padding:15px; border-radius:10px;">', unsafe_allow_html=True)
    st.markdown('#### Sephora', unsafe_allow_html=True)
    st.metric(label='Average Price', value=f"${avg_price_sephora:.0f}")
    st.metric(label='Median Price', value=f"${median_price_sephora:.0f}")
    st.metric(label='Price Range', value=f"${price_min_sephora:.0f} - ${price_max_sephora:.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

# 评分指标部分也应用相同的样式
st.subheader('Rating Metrics')

col5, col6 = st.columns(2)

with col5:
    st.markdown('<div style="background-color:#d8e6f5; padding:15px; border-radius:10px;">', unsafe_allow_html=True)
    st.markdown('#### Credo', unsafe_allow_html=True)
    st.metric(label='Average Rating', value=f"{avg_rating_credo:.2f}")
    st.metric(label='Median Rating', value=f"{median_rating_credo:.2f}")
    st.metric(label='Average Review Count', value=f"{avg_reviews_credo:.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div style="background-color:#f7d7d9; padding:15px; border-radius:10px;">', unsafe_allow_html=True)
    st.markdown('#### Sephora', unsafe_allow_html=True)
    st.metric(label='Average Rating', value=f"{avg_rating_sephora:.2f}")
    st.metric(label='Median Rating', value=f"{median_rating_sephora:.2f}")
    st.metric(label='Average Review Count', value=f"{avg_reviews_sephora:.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

# 价格分布
st.header('Price Distribution by Price Range')

# 定义新的价格区间和标签
price_bins = [0, 25, 50, 100, 200, df_combined['price'].max()]
price_labels = ['Budget ($0-25)', 'Low Price ($25-50)', 'Mid Price ($50-100)', 'High Price ($100-200)', 'Luxury ($200+)']

# 创建价格区间列
df_combined['price_bin'] = pd.cut(df_combined['price'], bins=price_bins, labels=price_labels, include_lowest=True)

# 分组并计算百分比（基于来源）
price_distribution = df_combined.groupby(['source', 'price_bin']).size().reset_index(name='count')
total_counts = price_distribution.groupby('source')['count'].transform('sum')
price_distribution['percent'] = price_distribution['count'] / total_counts * 100

# 创建柱状图，使用新的颜色
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

# 评分分布
st.header('Rating Distribution by Rating Range')

# 定义评分区间和标签
rating_bins = [0, 2, 3, 4, 5]
rating_labels = ['0-2', '2-3', '3-4', '4-5']

# 创建评分区间列
df_combined['rating_bin'] = pd.cut(df_combined['rating'], bins=rating_bins, labels=rating_labels, include_lowest=True)

# 分组并计算百分比（基于来源）
rating_distribution = df_combined.groupby(['source', 'rating_bin']).size().reset_index(name='count')
total_counts_rating = rating_distribution.groupby('source')['count'].transform('sum')
rating_distribution['percent'] = rating_distribution['count'] / total_counts_rating * 100

# 创建柱状图，使用新的颜色
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

# 箱线图：评分随价格区间的分布
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

# 选择品牌比较
st.header('Select a Brand to Compare')

common_brands = set(df_credo['brand_name'].unique()).intersection(set(df_sephora['brand_name'].unique()))
common_brands = sorted(list(common_brands))

if common_brands:
    selected_brand = st.selectbox('Select a Brand', options=common_brands)

    # 筛选选定品牌的数据
    df_brand = df_combined[df_combined['brand_name'] == selected_brand]

    # 按来源拆分数据
    df_brand_credo = df_brand[df_brand['source'] == 'Credo']
    df_brand_sephora = df_brand[df_brand['source'] == 'Sephora']

    # 计算平均价格和评分
    avg_price_brand_credo = df_brand_credo['price'].mean()
    avg_price_brand_sephora = df_brand_sephora['price'].mean()

    avg_rating_brand_credo = df_brand_credo['rating'].mean()
    avg_rating_brand_sephora = df_brand_sephora['rating'].mean()

    # 显示指标
    st.subheader(f'Average Price and Rating for {selected_brand}')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('#### Credo')
        st.metric(label='Average Price', value=f"${avg_price_brand_credo:.2f}")
        st.metric(label='Average Rating', value=f"{avg_rating_brand_credo:.2f}")

    with col2:
        st.markdown('#### Sephora')
        st.metric(label='Average Price', value=f"${avg_price_brand_sephora:.2f}")
        st.metric(label='Average Rating', value=f"{avg_rating_brand_sephora:.2f}")

    # 选定品牌的价格分布
    st.subheader(f'Price Distribution for {selected_brand}')

    # 使用相同的价格区间
    df_brand['price_bin'] = pd.cut(df_brand['price'], bins=price_bins, labels=price_labels, include_lowest=True)

    # 分组并计算百分比（基于来源）
    brand_price_distribution = df_brand.groupby(['source', 'price_bin']).size().reset_index(name='count')
    total_counts_brand_price = brand_price_distribution.groupby('source')['count'].transform('sum')
    brand_price_distribution['percent'] = brand_price_distribution['count'] / total_counts_brand_price * 100

    # 创建柱状图，使用新的颜色
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