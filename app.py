import streamlit as st
import pandas as pd
import plotly.express as px


# 화면 설정
st.set_page_config(
    page_title="업무지원 요청 분석 Dashboard",
    layout="wide"
)

st.title("📊 업무지원 요청 데이터 분석 Dashboard")


# 파일 업로드
uploaded_file = st.file_uploader(
    "업무지원 요청 파일 업로드 (CSV / Excel)",
    type=["csv", "xlsx"]
)


if uploaded_file:

    # 파일 형식별 데이터 로딩
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)


    st.success(
        f"파일 업로드 완료 : {uploaded_file.name}"
    )


    # 데이터 미리보기
    st.subheader("📌 데이터 미리보기")

    st.dataframe(
        df,
        use_container_width=True
    )


    # 컬럼 확인
    required_columns = [
        "category",
        "urgency",
        "status",
        "ai_handling",
        "request_date"
    ]


    missing = [
        col for col in required_columns
        if col not in df.columns
    ]


    if missing:
        st.error(
            f"필수 컬럼이 없습니다 : {missing}"
        )

    else:

        # 날짜 변환
        df["request_date"] = pd.to_datetime(
            df["request_date"]
        )


        # =========================
        # KPI 영역
        # =========================

        st.subheader("📈 주요 현황")


        col1, col2, col3, col4 = st.columns(4)


        total = len(df)

        complete = len(
            df[df["status"] == "완료"]
        )

        processing = len(
            df[df["status"] != "완료"]
        )

        urgent = len(
            df[
                (df["urgency"] == "상")
                &
                (df["status"] != "완료")
            ]
        )


        col1.metric(
            "전체 요청",
            f"{total}건"
        )

        col2.metric(
            "완료",
            f"{complete}건"
        )

        col3.metric(
            "미완료",
            f"{processing}건"
        )

        col4.metric(
            "긴급 미완료",
            f"{urgent}건"
        )



        # =========================
        # 업무 분류별 요청
        # =========================

        st.subheader("📂 업무분류별 요청 현황")


        category_count = (
            df["category"]
            .value_counts()
            .reset_index()
        )

        category_count.columns = [
            "업무분류",
            "건수"
        ]


        fig1 = px.bar(
            category_count,
            x="업무분류",
            y="건수",
            text="건수"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )



        # =========================
        # 긴급도 분석
        # =========================

        st.subheader("🚨 긴급도 분석")


        urgency_count = (
            df["urgency"]
            .value_counts()
            .reset_index()
        )

        urgency_count.columns = [
            "긴급도",
            "건수"
        ]


        fig2 = px.pie(
            urgency_count,
            names="긴급도",
            values="건수",
            hole=0.4
        )


        st.plotly_chart(
            fig2,
            use_container_width=True
        )



        # =========================
        # 상태별 현황
        # =========================

        st.subheader("📌 처리 상태")


        status_count = (
            df["status"]
            .value_counts()
            .reset_index()
        )

        status_count.columns = [
            "상태",
            "건수"
        ]


        fig3 = px.bar(
            status_count,
            x="상태",
            y="건수",
            text="건수"
        )


        st.plotly_chart(
            fig3,
            use_container_width=True
        )



        # =========================
        # AI 처리 가능 여부
        # =========================

        st.subheader("🤖 AI 처리 가능 현황")


        ai_count = (
            df["ai_handling"]
            .value_counts()
            .reset_index()
        )


        ai_count.columns = [
            "AI 처리구분",
            "건수"
        ]


        fig4 = px.pie(
            ai_count,
            names="AI 처리구분",
            values="건수"
        )


        st.plotly_chart(
            fig4,
            use_container_width=True
        )



        # =========================
        # 긴급 미완료 목록
        # =========================

        st.subheader("⚠️ 긴급 미완료 요청")


        urgent_df = df[
            (df["urgency"] == "상")
            &
            (df["status"] != "완료")
        ]


        if len(urgent_df) > 0:

            st.dataframe(
                urgent_df,
                use_container_width=True
            )

        else:

            st.info(
                "긴급 미완료 요청이 없습니다."
            )

else:

    st.info(
        "분석할 CSV 또는 Excel 파일을 업로드해주세요."
    )
