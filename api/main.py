from fastapi import FastAPI, Query
from typing import List, Optional, Dict
from pytrends.request import TrendReq

app = FastAPI()

@app.get("/")
async def health_check():
    return "The health check is successful!"

@app.get("/trends")
async def get_trends(
    kw_list: List[str] = Query(..., description="List of keywords to search trends for"),
    geo: Optional[str] = Query("", description="Geographical area"),
    timeframe: Optional[str] = Query("today 1-m", description="Timeframe for trends")
) -> Dict:

    try:
        pytrends = TrendReq(
            hl='en-US', 
            tz=360, 
            requests_args={'verify': False}
        )

        pytrends.build_payload(kw_list, timeframe=timeframe, geo=geo)
        data = pytrends.interest_over_time()

        trends = {}
        for date, row in data.iterrows():
            trends[str(date.date())] = row[kw_list].to_dict()

        return trends
    
    except KeyError as e:
        print(f"KeyError fetching trends: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error fetching trends: {e}")
        return {"error": str(e)}

@app.get("/related-query")
async def get_related_query(
    kw_list: List[str] = Query(..., description="List of keywords to search related queries for"),
    geo: Optional[str] = Query("", description="Geographical area"),
    timeframe: Optional[str] = Query("today 1-m", description="Timeframe for related queries"),
    cat: Optional[int] = Query(0, description="Category for trends")
) -> Dict:

    try:
        pytrends = TrendReq(
            hl='en-US', 
            tz=360, 
            requests_args={'verify': False}
        )

        pytrends.build_payload(kw_list, timeframe=timeframe, geo=geo, cat=cat)
        related_queries = pytrends.related_queries()

        rising_queries = {}
        for kw in kw_list:
            rising_data = related_queries.get(kw, {}).get('rising', None)
            if rising_data is not None and not rising_data.empty:
                rising_queries[kw] = rising_data.to_dict('records')
            else:
                rising_queries[kw] = []

        return rising_queries
    
    except KeyError as e:
        print(f"KeyError fetching related queries: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error fetching related queries: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
