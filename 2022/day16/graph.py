import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

edges = [("AK14", "SM0"), ("AK14", "PO0"), ("AK14", "OH0"), ("UF0", "BV6"), ("UF0", "AA0"), ("ZZ0", "IC17"),
         ("ZZ0", "EK0"), ("DS3", "ME0"), ("DS3", "JY0"), ("DS3", "OV0"), ("DS3", "RA0"), ("DS3", "AW0"), ("AA0", "ON0"),
         ("AA0", "UF0"), ("AA0", "WR0"), ("AA0", "ML0"), ("AA0", "AW0"), ("IC17", "VG0"), ("IC17", "ZZ0"),
         ("IC17", "BS0"), ("IC17", "ZB0"), ("IC17", "DF0"), ("TX0", "KM16"), ("TX0", "ZB0"), ("NA0", "GL20"),
         ("NA0", "CT0"), ("QI0", "MI0"), ("QI0", "OE9"), ("JN0", "BV6"), ("JN0", "BS0"), ("CT0", "JH12"),
         ("CT0", "NA0"), ("CN22", "SD0"), ("VG0", "ME0"), ("VG0", "IC17"), ("MI0", "QI0"), ("MI0", "JH12"),
         ("XC11", "CB0"), ("JY0", "DS3"), ("JY0", "IH0"), ("SH0", "KT23"), ("SH0", "OE9"), ("CB0", "XC11"),
         ("CB0", "JH12"), ("AO0", "ML0"), ("AO0", "NT4"), ("QE0", "NK13"), ("QE0", "PO0"), ("JF0", "KM16"),
         ("JF0", "SD0"), ("DF0", "ON0"), ("DF0", "IC17"), ("PO0", "AK14"), ("PO0", "QE0"), ("MR0", "OE9"),
         ("MR0", "BF10"), ("ZG0", "BV6"), ("ZG0", "QT0"), ("JT0", "RA0"), ("JT0", "OE9"), ("BU0", "BF10"),
         ("BU0", "BG0"), ("IT0", "NT4"), ("IT0", "KT23"), ("RH0", "FI0"), ("RH0", "KT23"), ("ME0", "VG0"),
         ("ME0", "DS3"), ("AM0", "NT4"), ("AM0", "SM0"), ("OV0", "BV6"), ("OV0", "DS3"), ("BS0", "JN0"),
         ("BS0", "IC17"), ("GL20", "NA0"), ("BV6", "OV0"), ("BV6", "JN0"), ("BV6", "ZG0"), ("BV6", "UF0"),
         ("RA0", "JT0"), ("RA0", "DS3"), ("ON0", "DF0"), ("ON0", "AA0"), ("VZ0", "NK13"), ("VZ0", "NT4"),
         ("AW0", "DS3"), ("AW0", "AA0"), ("QT0", "ZG0"), ("QT0", "KM16"), ("BG0", "KT23"), ("BG0", "BU0"),
         ("SD0", "JF0"), ("SD0", "CN22"), ("NK13", "VZ0"), ("NK13", "QE0"), ("NK13", "FI0"), ("OH0", "KT23"),
         ("OH0", "AK14"), ("BF10", "BU0"), ("BF10", "MR0"), ("GB25", "EK0"), ("IH0", "JY0"), ("IH0", "KM16"),
         ("KT23", "BG0"), ("KT23", "OH0"), ("KT23", "RH0"), ("KT23", "SH0"), ("KT23", "IT0"), ("WR0", "AA0"),
         ("WR0", "KM16"), ("FI0", "NK13"), ("FI0", "RH0"), ("ZB0", "IC17"), ("ZB0", "TX0"), ("OE9", "SH0"),
         ("OE9", "MR0"), ("OE9", "JT0"), ("OE9", "QI0"), ("EK0", "GB25"), ("EK0", "ZZ0"), ("SM0", "AK14"),
         ("SM0", "AM0"), ("JH12", "CB0"), ("JH12", "MI0"), ("JH12", "CT0"), ("KM16", "WR0"), ("KM16", "IH0"),
         ("KM16", "QT0"), ("KM16", "TX0"), ("KM16", "JF0"), ("ML0", "AO0"), ("ML0", "AA0"), ("NT4", "AO0"),
         ("NT4", "IT0"), ("NT4", "AM0"), ("NT4", "VZ0"), ]
G = nx.DiGraph()
nodes = set(edge[0] for edge in edges)
G.add_nodes_from(nodes)
G.add_edges_from(edges)
nx.draw_networkx(G, arrows=False, node_color="white")
plt.show()
