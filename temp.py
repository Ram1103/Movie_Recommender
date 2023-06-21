import streamlit as st

def intro():
    import streamlit as st

    st.write("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Welome to Movie Gallary!.

        **👈 Select a function you would like from the dropdown on the left** to see some examples
        of what we can do!

        ### Want to learn more?

        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)

        ### See more complex demos

        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )

def mapping_demo():
    import streamlit as st
    import pandas as pd
    import pydeck as pdk
    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data.
"""
    )

    import requests
import streamlit as st
import pandas as pd
api_key = "f54e9e41716e8d9622bb4b4f3a8b4175"
movie_id = 550
api_version = 3
api_base_url = f"https://api.themoviedb.org/{api_version}"
endpoint_path = f"/search/movie"

st.sidebar.header('User Input Features')
selected = st.sidebar.selectbox(
     "What would you like to do",
     ("Search", "Recommendation", "Chat","FAQ"))



st.write('# Search your movie!')
search_query = st.text_input(" Enter here! ")
st.write('### The current movie title is', search_query)
endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}&query={search_query}"


#print(endpoint)
r=requests.get(endpoint) 
#pprint.pprint(r.json())
if r.status_code in range(200,299):
    
    data=r.json()
    
    results=data['results']
    if len(results)>0: 
        st.success("The movie is available!")
        #st.write("## Keys")
        #st.write(results[0].keys())
        movie_ids=list()
        movie_title=set()
        movie_RD=set()
        st.write('### Here are the movies related to', search_query)
        col1, col2 ,col3 ,col4 = st.columns(4) 
        with col1:
            st.write("#### Poster")  
        with col2:
            st.write("#### Name")  
        with col3:
            st.write("#### Movie ID")  
        with col4:
            st.write("#### Release Date")  
        

        for result in results:
            _id = result['id']
            _RD = result['release_date']
            _title = result['title']
            
            poster = (result['poster_path'])
            full_path = f"https://image.tmdb.org/t/p/w500/{poster}"
            col1, col2 ,col3 ,col4 = st.columns(4) 
            with col1:
                st.image(full_path)  
            with col2:
                st.write(result['title'])
            with col3:
                st.write(_id)
            with col4:
                st.write(_RD)

                     
            #st.image(full_path, 50)
            movie_ids.append(_id)
            movie_title.add(_title)
            movie_RD.add(_RD)
        )

def plotting_demo():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!
"""
    )

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


def data_frame_demo():
    import streamlit as st
    import pandas as pd
    import altair as alt

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    st.write(
        """
        This demo shows how to use `st.write` to visualize Pandas DataFrames.

(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)
"""
    )

    @st.cache_data
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

page_names_to_funcs = {
    "—": intro,
    "Plotting Demo": plotting_demo,
    "Mapping Demo": mapping_demo,
    "DataFrame Demo": data_frame_demo
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()