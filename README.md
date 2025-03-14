# yum-finder

This little hack was inspired by the video:

I Found the Last KenTacoHut on Planet Earth - https://www.youtube.com/watch?v=deodx6rIkcs by Sam Reid - https://www.youtube.com/@therealsamreid

If you're reading this and haven't watched it yet: Give it a watch to fully appreciate this.

The gist of the video is to find the only remaining KFC, Taco Bell, Pizza Hut combination locations. As a software engineer I wrote undocumented/throw-away/fun code to try to answer this question.

## Directories

```
combos/ - Text files with the locations of the corresponding combo restaurants

raw/ - The raw US restaurant addresses scraped from either tacobell.com, kfc.com, or pizzahut.com
normalized/ - An attempt at normalizing the addresses to something standard.
    This is because on the different websites, the wording of the address may be slightly different.
    Like "N. Main St." instead of "North Main Street"
```

## The Code

Basically I ran parts of location_finder.py to find the addresses. Then I ran parts of raw_to_normalized.py to normalize the addresses. Then I ran parts of kentacohut.py to find the addresses with multiple restaurants.

I'm leaving this code as is: not further tested, or developed. Feel free to play around with it though I make no guarantees.

## The Result

The only ones I found that have all 3 restaurants are as follows (as of 3/12/2025):

```
1 Arena Plz, Louisville, Kentucky, 40202                  .. an arena: doesn't count
100 Universal City Plz, Universal City, California, 91608 .. Universal Studios.. doesn't count
1441 Gardiner Ln, Louisville, Kentucky, 40213             .. the Yum Companies headquarters.. with a food court?
2084 S Marina Dr, Thermal, California, 92274              .. The closest thing. Though its a food court with all 3 next to each other.
Lee Hwy, Arlington, Virginia, 22205                       .. Result of a normalization error. Not worth debugging deeper.
```

.. So I don't think there are any US-State-Based KenTacoHuts left. :'(
