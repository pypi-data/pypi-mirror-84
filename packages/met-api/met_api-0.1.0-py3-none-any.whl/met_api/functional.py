from typing import Optional, List
from datetime import datetime
import json

import requests

from .response_objects import ObjectResponse, ObjectsResponse, DepartmentsResponse
from .utils import logical_xnor

OBJECTS_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
DEPARTMENTS_URL = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
SEARCH_URL = "https://collectionapi.metmuseum.org/public/collection/v1/search"


def get_objects(
    date: Optional[datetime] = None, department_ids: Optional[List[int]] = None
) -> ObjectsResponse:
    """
    A listing of all valid Object IDs available for access.

    :param date: Optional[datetime] - Returns any objects with updated data after this date
    :param department_ids: List[int] - Returns any objects in a specific department
    :return: ObjectResponse
    """
    if date:
        date = date.strftime("%Y-%m-%d")
    params = {"metadataDate": date, "departmentIds": department_ids}
    response = requests.get(OBJECTS_URL, params=params)
    data = json.loads(response.text)
    response_object = ObjectsResponse(**data)
    return response_object


def get_object(id_: int) -> ObjectResponse:
    """
    Returns a record for an object, containing all open access data about that object,
        including its image (if the image is available under Open Access)
    :param id_:int - Object id
    :return: ObjectResponse
    """
    url = f"{OBJECTS_URL}/{id_}"
    response = requests.get(url)
    if response.status_code == 404:
        raise ValueError(f"Object with given id {id_} not found on the server.")
    elif response.status_code == 200:
        data = json.loads(response.text)
        response_object = ObjectResponse(**data)
        return response_object


def get_departments() -> DepartmentsResponse:
    """
     Returns a listing of all departments.
    :return:DepartmentsResponse
    """
    response = requests.get(DEPARTMENTS_URL)
    data = json.loads(response.text)
    response_object = DepartmentsResponse(**data)
    return response_object


def search(
    q: str,
    is_highlight: Optional[bool] = None,
    department_id: Optional[int] = None,
    is_on_view: Optional[bool] = None,
    artist_or_culture: Optional[bool] = None,
    medium: Optional[List[str]] = None,
    has_images: Optional[bool] = None,
    geo_location: Optional[List[str]] = None,
    date_begin: Optional[datetime] = None,
    date_end: Optional[datetime] = None,
) -> ObjectsResponse:
    """

    :param q:str - Returns a listing of all Object IDs for objects that contain the search query within the object’s data
    :param is_highlight:Optional[bool] - Returns objects that match the query and are designated as highlights.
                               Highlights are selected works of art from The Met Museum’s permanent
                               collection representing different cultures and time periods.
    :param department_id:int - Returns objects that are a part of a specific department.
    :param is_on_view:bool - Returns objects that match the query and are on view in the museum.
    :param artist_or_culture:bool - Returns objects that match the query, specifically
                                    searching against the artist name or culture field for objects.
    :param medium:List[str] - Returns objects that match the query and are of the specified medium or object type.
                              Examples include: "Ceramics", "Furniture", "Paintings", "Sculpture", "Textiles", etc.
    :param has_images:bool - Returns objects that match the query and have images.
    :param geo_location:List[str] - Returns objects that match the query and the specified geographic location.
                                    Examples include: "Europe", "France", "Paris", "China", "New York", etc.
    :param date_begin:datetime - Returns objects that match the query and fall between the date_begin and date_end parameters.
                                You must use both dateBegin and dateEnd.
                                You must use both dateBegin and dateEnd.

    :param date_end:datetime - Returns objects that match the query and fall between the date_begin and date_end parameters.
                                You must use both dateBegin and dateEnd.
    :return: ObjectsResponse
    """
    if (date_begin and date_end) and date_begin > date_end:
        raise ValueError(f"date_end {date_end} > date_begin {date_begin}")
    if not logical_xnor(date_begin, date_end):
        raise ValueError(
            "Both date_begin and date_end have to be present if one of is present."
        )
    if date_begin:
        date_begin = date_begin.strftime("%Y-%m-%d")
        date_end = date_end.strftime("%Y-%m-%d")
    if type(has_images) is bool:
        if has_images:
            has_images = "true"
        else:
            has_images = "false"
    if type(is_on_view) is bool:
        if is_on_view:
            is_on_view = "true"
        else:
            is_on_view = "false"
    params = {
        "q": q,
        "isHighlight": is_highlight,
        "departmentId": department_id,
        "isOnView": is_on_view,
        "artistOrCulture": artist_or_culture,
        "medium": medium,
        "hasImages": has_images,
        "geoLocation": geo_location,
        "dateBegin": date_begin,
        "dateEnd": date_end,
    }
    response = requests.get(SEARCH_URL, params=params)
    data = json.loads(response.text)
    response_object = ObjectsResponse(**data)
    return response_object
