from flask import Flask, render_template, request, session, redirect

import more_itertools
import altair as alt
import pandas as pd

app = Flask(__name__)

######Global Variables 

esb_data = pd.read_csv("data/Esb_Data.csv")
city = esb_data[esb_data['Type'] == "City"]
county = esb_data[esb_data['Type'] == "County"] 

#################################
Cities = sorted(city.Council.unique())
Counties = sorted(county.Council.unique())
Years = sorted(esb_data.Year.unique())
Types = sorted(esb_data.Type.unique())
################################

#The First page of the webapp----------------------------------------------------- 

@app.route("/")
def home_page():
    return render_template("homepage.html")

#Head to the second page------------------------------------------------------------

def produce_table(x , size=10):
    output = "<table>"
    for chunk in more_itertools.chunked(x, size):
        output += '<tr>'
        for t in chunk:
            output += f"<td><input type='checkbox' name='{t}' value='{t}'>{t}</td>"
        output += '</tr>'
    output += "</table>"
    return output

@app.route("/dynamic_page1")
def dynamic_page_1():
    data_1 = produce_table(Types , 2 )
    return render_template("checks_1.html" , data= data_1)


@app.route("/processchecks1", methods=["POST"] )
def process_checks_1():
    session["selection_city"] = list(request.form.keys())
    if (session["selection_city"][0]) == 'City':
        return redirect ("/cities1")
    else:
        return redirect('/counties1')
#-----------------------------------------------------------------------
@app.route("/cities1")
def display_session_1():
    the_table_1 = produce_table(Cities, 5)
    return render_template("checks_2.html", data=the_table_1 )

@app.route("/processcheck2", methods=["POST"] )
def process_checks_2():
    session["selection_council"] = list(request.form.keys())
    return redirect("/year")
#=======================================================================

@app.route("/counties1")
def display_session_2():
    the_table_2 = produce_table(Counties, 5)
    return render_template("checks_2.html", data=the_table_2)


#=========================================================================

@app.route("/year")
def display_years():
    the_table_2 = produce_table(Years,1)
    return render_template("checks_3.html", data=the_table_2 )

@app.route("/processcheck3", methods= ["POST"])
def process_checks_3():
    session["selection_year"] = list(request.form.keys())
    return redirect("/visual")


@app.route("/visual")
def display_the_plot():
    df = pd.concat(esb_data[esb_data["Type"] == var1] for var1 in session["selection_city"])
    df1 = pd.concat(df[df["Council"] == var2] for var2 in session["selection_council"])
    df2 = pd.concat(df1[df1["Year"] == int(var3)] for var3 in session["selection_year"])
    print(df)
    print(df1)
    print(df2)

    
    
    ## print(df.shape)
    ## print(session["selection"])
    plot =alt.Chart(df2).mark_bar().encode(
    alt.X('No_Of_Connections:Q',
          sort=alt.SortField(field='No_Of_Connections', order='ascending'),
          scale=alt.Scale(domain=(0, 1000)),
          axis=alt.Axis(title="Connection Count", tickCount=20),
          
        ),
    alt.Y('Month:O'),
    alt.Color('Month:N'),
    alt.Facet('Year:O'),
).properties(width=200)
    plot.save("templates/plot.html")
    return render_template("plot.html")

app.secret_key = ".v/vndfl/n/dlfkn/ldfkn/ldkngLKN"


if __name__ == "__main__":
    app.run(debug=True)
