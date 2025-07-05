import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from algorithm import DiscretizationAlgorithms, get_algorithm_info
import inspect
# Cấu hình trang
st.set_page_config(
    page_title="Discretization & Binning Demo",
    page_icon="📊",
    layout="wide"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .algorithm-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .code-block {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 0.25rem;
        padding: 1rem;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📊📊 Discretization & Binning Demo</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎛️ Cài đặt")
    
    # Upload file
    uploaded_file = st.sidebar.file_uploader(
        "📁 Chọn file CSV",
        type=['csv'],
        help="Upload file CSV chứa dữ liệu numerical"
    )
    
    if uploaded_file is not None:
        try:
            # Đọc dữ liệu
            df = pd.read_csv(uploaded_file)
            st.sidebar.success(f"✅ Đã tải {len(df)} dòng dữ liệu")
            
            # Chọn cột numerical
            numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numerical_columns:
                selected_column = st.sidebar.selectbox(
                    "�� Chọn cột numerical",
                    numerical_columns,
                    help="Chọn cột chứa dữ liệu số để thực hiện discretization"
                )
                
                # Hiển thị thông tin cột
                col_data = df[selected_column].dropna()
                st.sidebar.info(f"""
                **Thông tin cột {selected_column}:**
                - Số lượng: {len(col_data)}
                - Min: {col_data.min():.2f}
                - Max: {col_data.max():.2f}
                - Mean: {col_data.mean():.2f}
                - Std: {col_data.std():.2f}
                """)
                
                # Vẽ biểu đồ histogram và KDE
                st.subheader("📊 Phân tích dữ liệu gốc")
                
                fig = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=('Histogram', 'Box Plot'),
                    specs=[[{"type": "histogram"}, {"type": "box"}]]
                )
                
                # Histogram
                fig.add_trace(
                    go.Histogram(x=col_data, nbinsx=30, name="Histogram", marker_color='#2f9e44'),
                    row=1, col=1
                )
                
                # Box Plot
                fig.add_trace(
                    go.Box(y=col_data, name="Box Plot", marker_color='#2f9e44'),
                    row=1, col=2
                )
                
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # Chọn thuật toán
                st.subheader("🔧 Chọn thuật toán Discretization")
                
                algo_display_names = {
                    "Equal Width Binning": "equal_width_binning",
                    "Equal Frequency Binning": "equal_frequency_binning",
                    "KMeans Binning": "kmeans_binning",
                    "Jenks Natural Breaks": "jenks_natural_breaks",
                    "Standard Deviation Binning": "standard_deviation_binning"
}
                selected_algorithm = st.selectbox(
                    "Chọn thuật toán:",
                    list(algo_display_names.keys()),
                    help="Chọn thuật toán discretization bạn muốn áp dụng"
                )
                algorithms_info = get_algorithm_info()
                if selected_algorithm:
                    # Hiển thị thông tin thuật toán
                    method_name = algo_display_names[selected_algorithm]
                    print(method_name)
                    selected_func = getattr(DiscretizationAlgorithms, method_name)
                    print(selected_func)
                    print(algorithms_info[selected_algorithm]['description'])
                    st.markdown(f"""
                    <div class="algorithm-card">
                        <h4>{selected_algorithm}</h4>
                        <p>{algorithms_info[selected_algorithm]['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    print('abc')
                    source_code = inspect.getsource(selected_func)
                    with st.expander("👨‍💻 Xem code thuật toán"):
                        st.code(source_code, language='python')
                    
                    # Hiển thị parameters
                    st.subheader("⚙️ Tham số thuật toán")
                    algo_info = algorithms_info[selected_algorithm]
                    params = {}
                    col1, col2 = st.columns(2)
                    with col1:
                        for param_name, param_info in algo_info['parameters'].items():
                            if param_info['type'] == 'int':
                                params[param_name] = st.number_input(
                                    f"{param_info['description']} ({param_name})",
                                    min_value=param_info['min'],
                                    max_value=param_info['max'],
                                    value=param_info['default'],
                                    help=f"Chọn giá trị cho {param_name}"
                                )
                    
                    # Nút Apply
                    if st.button("🚀 Áp dụng thuật toán", type="primary"):
                        with st.spinner("Đang xử lý..."):
                            # Áp dụng thuật toán
                            discretized_data = apply_algorithm(
                                selected_algorithm, col_data, params
                            )
                            
                            # Hiển thị kết quả
                            st.subheader("✅ Kết quả Discretization")
                            
                            # Tạo DataFrame kết quả
                            result_df = pd.DataFrame({
                                'Original': col_data,
                                'Discretized': discretized_data
                            })
                            
                            # Hiển thị bảng kết quả
                            st.dataframe(result_df.head(20), use_container_width=True)
                            
                            # Thống kê bin
                            bin_counts = pd.Series(discretized_data).value_counts()
                            bin_counts = bin_counts.sort_index(key=lambda x: x.str.split('_').str[1].astype(int))
                            st.write("**Phân bố các bin:**")
                            fig_bar = go.Figure(data=[go.Bar(x=bin_counts.index, y=bin_counts, marker_color='#2f9e44')])
                            fig_bar.update_layout(xaxis_title='Bins', yaxis_title='Số lượng', title='Phân bố các bin')
                            st.plotly_chart(fig_bar, use_container_width=True)
                            
                            # Vẽ biểu đồ so sánh
                            st.subheader("📈 So sánh trước và sau discretization")
                            
                            fig_compare = make_subplots(
                                rows=1, cols=2,
                                subplot_titles=('Dữ liệu gốc', 'Dữ liệu sau discretization'),
                                specs=[[{"type": "histogram"}, {"type": "histogram"}]]
                            )
                            
                            # Histogram dữ liệu gốc
                            fig_compare.add_trace(
                                go.Histogram(x=col_data, nbinsx=30, name="Original", marker_color='#2f9e44'),
                                row=1, col=1
                            )
                            
                            # Histogram dữ liệu discretized
                            bin_labels = sorted(set(discretized_data), key=lambda x: int(x.split('_')[1]))
                            discretized_data = pd.Categorical(discretized_data, categories=bin_labels, ordered=True)

                            fig_compare.add_trace(
                                go.Histogram(x=discretized_data, name="Discretized", marker_color='#2f9e44'),
                                row=1, col=2
                            )
                            
                            fig_compare.update_layout(height=400, showlegend=False)
                            st.plotly_chart(fig_compare, use_container_width=True)
                            
                            # Download kết quả
                            csv = result_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Tải xuống kết quả CSV",
                                data=csv,
                                file_name=f"discretized_{selected_column}.csv",
                                mime="text/csv"
                            )
            else:
                st.error("❌ Không tìm thấy cột numerical trong file!")
                
        except Exception as e:
            st.error(f"❌ Lỗi khi đọc file: {str(e)}")
    else:
        # Hướng dẫn sử dụng
        st.info("""
        👋 **Chào mừng đến với Discretization & Binning Demo!**
        
        **Cách sử dụng:**
        1. �� Upload file CSV chứa dữ liệu numerical
        2. �� Chọn cột numerical bạn muốn discretize
        3. 🔧 Chọn thuật toán discretization
        4. ⚙️ Điều chỉnh tham số (nếu có)
        5. 🚀 Nhấn "Áp dụng thuật toán" để xem kết quả
        
        **Các thuật toán có sẵn:**
        - **Equal Width Binning**: Chia dữ liệu thành các bin có độ rộng bằng nhau
        - **Equal Frequency Binning**: Chia dữ liệu thành các bin có số lượng phần tử bằng nhau
        - **K-Means Binning**: Sử dụng K-Means clustering để tạo các bin
        - **Jenks Natural Breaks**: Tìm các điểm break tự nhiên trong dữ liệu
        - **Standard Deviation Binning**: Chia dữ liệu dựa trên độ lệch chuẩn
        """)
        
        # Tạo dữ liệu mẫu
        st.subheader("📊 Dữ liệu mẫu để test")
        sample_data = np.random.normal(100, 15, 1000)
        sample_df = pd.DataFrame({
            'Age': sample_data,
            'Salary': np.random.normal(50000, 10000, 1000),
            'Score': np.random.uniform(0, 100, 1000)
        })
        
        st.dataframe(sample_df.head(10), use_container_width=True)
        
        # Download dữ liệu mẫu
        csv_sample = sample_df.to_csv(index=False)
        st.download_button(
            label="📥 Tải xuống dữ liệu mẫu",
            data=csv_sample,
            file_name="sample_data.csv",
            mime="text/csv"
        )

def apply_algorithm(algorithm_name, data, params):
    """
    Áp dụng thuật toán discretization được chọn
    """
    algo = DiscretizationAlgorithms()
    
    if algorithm_name == "Equal Width Binning":
        discretized, _, _ = algo.equal_width_binning(data, params['n_bins'])
    elif algorithm_name == "Equal Frequency Binning":
        discretized, _ = algo.equal_frequency_binning(data, params['n_bins'])
    elif algorithm_name == "K-Means Binning":
        discretized, _ = algo.kmeans_binning(data, params['n_bins'])
    elif algorithm_name == "Jenks Natural Breaks":
        discretized, _ = algo.jenks_natural_breaks(data, params['n_bins'])
    elif algorithm_name == "Standard Deviation Binning":
        discretized, _ = algo.standard_deviation_binning(data, params['n_std'])
    else:
        raise ValueError(f"Thuật toán {algorithm_name} không được hỗ trợ")
    
    return discretized

if __name__ == "__main__":
    main()
