FROM continuumio/anaconda3
COPY . /user/app 
EXPOSE 5000
WORKDIR /user/app
RUN pip install -r requirements.txt && \ 
    apt update && apt install -y libsm6 libxext6 
CMD docker run --network host ...
CMD streamlit run main.py --server.port $PORT