from typing import List, Optional, Dict, Union

from pydantic import BaseModel


class ObjectsResponse(BaseModel):
    total: int
    objectIDs: Optional[List[int]]


class ObjectResponse(BaseModel):
    objectID: int
    isHighlight: Optional[bool]
    accessionNumber: Optional[str]
    accessionYear: Optional[str]
    isPublicDomain: Optional[bool]
    primaryImage: Optional[str]
    primaryImageSmall: Optional[str]
    additionalImages: Optional[List[str]]
    constituents: Optional[List[Dict[str, Union[str, int]]]]
    department: Optional[str]
    objectName: Optional[str]
    title: Optional[str]
    culture: Optional[str]
    period: Optional[str]
    dynasty: Optional[str]
    reign: Optional[str]
    portfolio: Optional[str]
    artistRole: Optional[str]
    artistPrefix: Optional[str]
    artistDisplayName: Optional[str]
    artistDisplayBio: Optional[str]
    artistSuffix: Optional[str]
    artistAlphaSort: Optional[str]
    artistNationality: Optional[str]
    artistBeginDate: Optional[str]
    artistEndDate: Optional[str]
    artistGender: Optional[str]
    artistWikidata_URL: Optional[str]
    artistULAN_URL: Optional[str]
    objectDate: Optional[str]
    objectBeginDate: Optional[int]
    objectEndDate: Optional[int]
    medium: Optional[str]
    dimensions: Optional[str]
    creditLine: Optional[str]
    geographyType: Optional[str]
    city: Optional[str]
    state: Optional[str]
    county: Optional[str]
    country: Optional[str]
    region: Optional[str]
    subregion: Optional[str]
    locale: Optional[str]
    locus: Optional[str]
    excavation: Optional[str]
    river: Optional[str]
    classification: Optional[str]
    rightsAndReproduction: Optional[str]
    linkResource: Optional[str]
    metadataDate: Optional[str]
    repository: Optional[str]
    objectURL: Optional[str]
    tags: Optional[List[Dict[str, str]]]
    objectWikidata_URL: Optional[str]
    isTimelineWork: Optional[bool]
    GalleryNumber: Optional[str]


class DepartmentsResponse(BaseModel):
    departments: List[Dict[str, Union[str, int]]]
