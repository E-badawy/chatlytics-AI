
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import helper
from ml import message_clustering
from executive import generate_insights
from preprocessor import preprocess
from health import conversation_health
from recommendations import generate_recommendations

st.set_page_config(page_title="Chatlytics AI", page_icon="💬", layout="wide")

st.markdown("""
<style>
.stApp{background:#F7F8FA;}
.hero{background:linear-gradient(90deg,#0A3D62,#D4AF37);padding:25px;border-radius:15px;color:white;text-align:center;margin-bottom:20px;}
.kpi{background:white;padding:15px;border-left:6px solid #D4AF37;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,.08);}
.footer{text-align:center;color:#666;margin-top:50px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='hero'>
<h1>💬 Chatlytics AI</h1>
<h3>Conversation Intelligence Dashboard</h3>
<p>Business Intelligence • NLP • Machine Learning</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Chatlytics AI")
    uploaded = st.file_uploader("Upload WhatsApp .txt", type="txt")
    with st.expander("📖 Export Guide"):
        st.markdown("""1. Open chat\n2. More → Export Chat\n3. Choose **Without Media**\n4. Upload .txt here""")
    with st.expander("ℹ About"):
        st.write("Chatlytics AI analyses exported WhatsApp conversations.")
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.write("**Amin Muhammed Badawi**")
    st.write("Data Science Consultant")
    st.write("📧 cigma.generalsolutions@gmail.com")
    st.write("📱 08065440075")

if uploaded:
    with st.spinner("🔍 Analysing your WhatsApp conversation..."):
        try:
            df=preprocess(uploaded.read().decode("utf-8"))
            # Run Machine Learning
            df = message_clustering(df)
            st.success("✅ Chat uploaded and analysed successfully.")
        except Exception as e:
            st.error(f"Parsing failed: {e}")
            st.stop()

    users=sorted([u for u in df.user.unique() if u!="group_notification"])
    selected=st.sidebar.selectbox("Analyse",["Overall"]+users)

    stats=helper.fetch_stats(selected,df)
    total,words,media,links,emojis=stats

    executive = generate_insights(df, selected)

    summary = executive["summary"]
    metrics = executive["metrics"]
    
    stats = helper.fetch_stats(selected, df)
    total, words, media, links, emojis = stats

    # ==========================================
    # Executive Intelligence
    # ==========================================

    executive = generate_insights(df, selected)

    summary = executive["summary"]
    metrics = executive["metrics"]
    
    st.divider()
    st.subheader("📌 Executive Intelligence")

    # Executive KPI cards
    e1, e2, e3, e4 = st.columns(4)

    e1.metric("👥 Participants", metrics["Participants"])
    e2.metric("📅 Duration", f'{metrics["Days"]} days')
    e3.metric("🔥 Peak Month", metrics["Peak Month"])
    e4.metric("⭐ Engagement", metrics["Engagement"])

    st.info(summary)
    
    score, status = conversation_health(metrics)

    st.subheader("🩺 Conversation Health Score")

    st.progress(score / 100)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric("Score", f"{score}/100")

    with col2:
        st.success(status)
        
        
    st.subheader("💡 Actionable Insights")

    recommendations = generate_recommendations(metrics)

    for rec in recommendations:
     st.info(rec)    
        
    c1,c2,c3,c4,c5=st.columns(5)
    for col,val,label in zip([c1,c2,c3,c4,c5],
                             [total,words,media,links,emojis],
                             ["Messages","Words","Media","Links","Emojis"]):
        col.metric(label,f"{val:,}")
        
    st.divider()
    st.subheader("Monthly Timeline")
    tl=helper.monthly_timeline(selected,df)
    fig=px.line(tl,x="time",y="message",markers=True)
    st.plotly_chart(fig,use_container_width=True)

    st.divider()
    st.subheader("Daily Timeline")
    dt=helper.daily_timeline(selected,df)
    fig=px.line(dt,x="only_date",y="message")
    st.plotly_chart(fig,use_container_width=True)

    if selected=="Overall":
        st.subheader("Most Active Users")
        a,b=st.columns([2,1])
        vc,pct=helper.most_busy_users(df)
        with a:
            st.plotly_chart(px.bar(x=vc.index,y=vc.values),use_container_width=True)
        with b:
            st.dataframe(pct,use_container_width=True)

    st.subheader("Common Words")
    common=helper.most_common_words(selected,df)
    st.plotly_chart(px.bar(common,x="Count",y="Word",orientation="h"),use_container_width=True)

    st.subheader("Emoji Analysis")
    emo=helper.emoji_analysis(selected,df)
    if not emo.empty:
        c1,c2=st.columns(2)
        with c1: st.dataframe(emo.head(15),use_container_width=True)
        with c2: st.plotly_chart(px.pie(emo.head(10),values="Count",names="Emoji"),use_container_width=True)
    else:
        st.write("No emojis found.")

    st.subheader("Word Cloud")
    wc=helper.create_wordcloud(selected,df)
    fig,ax=plt.subplots(figsize=(10,4))
    ax.imshow(wc)
    ax.axis("off")
    st.pyplot(fig)

    st.divider()
    st.subheader("Download")

    st.divider()
    st.subheader("🤖 Machine Learning: Message Clusters")

    cluster_counts = (
    df["cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
    )

    cluster_counts.columns = ["Cluster", "Messages"]

    fig = px.bar(
    cluster_counts,
    x="Cluster",
    y="Messages",
    color="Cluster",
    title="Distribution of Machine Learning Clusters",
    )

    st.plotly_chart(fig, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
    label="Download Processed Dataset (.csv)",
    data=csv,
    file_name="Chatlytics_AI_Analysis.csv",
    mime="text/csv",
    use_container_width=True
)

st.info(
    """
The K-Means clustering model groups messages into communication patterns based on
their textual characteristics (length, emojis, media usage and links). This
unsupervised learning approach helps reveal latent message types without requiring
pre-labelled data.
"""
)

st.markdown("<div class='footer'>© 2026 Chatlytics AI • Built by Amin Muhammed Badawi</div>",unsafe_allow_html=True)
