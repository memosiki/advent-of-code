import sys
from dataclasses import dataclass
from typing import Optional

__doc__ = """
https://dccg.upc.edu/wp-content/uploads/2020/06/GeoC-Voronoi-storing.pdf
https://docs.rs/voronoi/latest/src/voronoi/dcel.rs.html
https://neerc.ifmo.ru/wiki/index.php?title=%D0%9F%D0%9F%D0%9B%D0%93_%D0%B8_%D0%A0%D0%A1%D0%94%D0%A1_(PSLG_%D0%B8_DCEL):_%D0%BE%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5,_%D0%BF%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BD%D0%B8%D0%B5_%D0%A0%D0%A1%D0%94%D0%A1_%D0%BC%D0%BD%D0%BE%D0%B6%D0%B5%D1%81%D1%82%D0%B2%D0%B0_%D0%BF%D1%80%D1%8F%D0%BC%D1%8B%D1%85
https://cs.stackexchange.com/questions/14591/problem-with-storing-an-existing-triangulation-in-a-dcel/18167#18167

>>>!!! https://erickimphotography.com/blog/wp-content/uploads/2018/09/Computational-Geometry-Algorithms-and-Applications-3rd-Ed.pdf
"""


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Vertex:
    point: Point
    # Some halfedge having this vertex as the origin
    incident_edge: Optional["HalfEdge"]


@dataclass
class HalfEdge:
    prev: Optional["HalfEdge"]
    next: Optional["HalfEdge"]

    # half-edge "going the opposite way"
    twin: "HalfEdge"

    # Vertex at the start of the half-edge
    origin: Vertex

    # lhs face
    face: "Face"


@dataclass
class Face:
    # face is defined by lhs counter clock-wise traversal on edges

    # any half-edge of the face
    halfedge: HalfEdge

    # point defining the voronoi cell face
    focus: Point


@dataclass
class DCEL:
    verticies: list[Vertex]
    halfedges: list[HalfEdge]
    faces: list[Face]


points: list[Point] = [Point(*map(int, line.split())) for line in sys.stdin]

dcel = DCEL
