import pandas as pd

#Load the Netflix  Dataset
df = pd.read_csv('netflix_titles_2021.csv')

#show the first 5 rows of the dataset
df.head()

#dataset dimensions
df.shape

#dataset information
df.info()

#percentage of missing values
missing_values = (df.isnull().sum() / len (df)) * 100
print("\nMissing values percentage:")
print(missing_values.round(2))

# Check duplicate rows
duplicates = df.duplicated().sum()

print("\nDuplicate rows:")
print(duplicates)

# Check duplicate IDs
duplicate_ids = df["show_id"].duplicated().sum()

print("\nDuplicate show IDs:")
print(duplicate_ids)

# Check duplicate titles
duplicate_titles = df["title"].duplicated().sum()

print("\nDuplicate titles:")
print(duplicate_titles)

# Fill missing categorical values
df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")

# Inspect rows with missing rating
print("\nMissing rating:")
print(df[df["rating"].isnull()][["title", "type", "rating", "duration"]])

# Inspect rows with missing duration
print("\nMissing duration:")
print(df[df["duration"].isnull()][["title", "type", "rating", "duration"]])

# Inspect rows with missing date_added
print("\nMissing date_added:")
print(df[df["date_added"].isnull()][
    ["title", "type", "release_year", "date_added"]
])

# Fix misplaced movie durations

mask = (
    (df["type"] == "Movie") &
    (df["duration"].isna()) &
    (df["rating"].str.contains("min", na=False))
)

df.loc[mask, "duration"] = df.loc[mask, "rating"]
df.loc[mask, "rating"] = "Unknown"

# Fix records where duration was incorrectly stored in the rating column
mask = df["duration"].isnull() & df["rating"].str.contains(
    "min", na=False
)

df.loc[mask, "duration"] = df.loc[mask, "rating"]
df.loc[mask, "rating"] = "Unknown"

df.loc[mask, "duration"] = df.loc[mask, "rating"]

df.loc[mask, "rating"] = "Unknown"

df["rating"] = df["rating"].fillna("Unknown")

# Convert date_added to datetime
df["date_added"] = pd.to_datetime(
    df["date_added"].str.strip(),
    errors="coerce"
)

# Create year and month columns
df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month_name()

print("\nData types after cleaning:")
print(df.dtypes)

print("\nMissing values after cleaning:")
print(df.isnull().sum())



# Content distribution
content_counts = df["type"].value_counts()

print("\nContent distribution:")
print(content_counts)


# STEP 8 - Country Analysis

# Remove records with unknown countries
country_df = df[df["country"] != "Unknown"].copy()

# Split multiple countries
country_df["country"] = country_df["country"].str.split(",")

# Create one row per country
country_df = country_df.explode("country")

# Remove extra spaces
country_df["country"] = country_df["country"].str.strip()

# Count titles by country
top_countries = country_df["country"].value_counts().head(10)

print("\nTop 10 Countries:")
print(top_countries)

# STEP 10 - Genre Analysis

# Create a copy of the dataset
genre_df = df.copy()

# Split genres into lists
genre_df["listed_in"] = genre_df["listed_in"].str.split(",")

# Create one row per genre
genre_df = genre_df.explode("listed_in")

# Remove extra spaces
genre_df["listed_in"] = genre_df["listed_in"].str.strip()

# Count the 10 most common genres
top_genres = genre_df["listed_in"].value_counts().head(10)

print("\nTop 10 Genres:")
print(top_genres)

# Content distribution percentage
content_percentage = df["type"].value_counts(normalize=True) * 100

print("\nContent distribution percentage:")
print(content_percentage.round(2))

import matplotlib.pyplot as plt

content_counts.plot(kind="bar")

plt.title("Netflix Content Distribution")
plt.xlabel("Content Type")
plt.ylabel("Number of Titles")
plt.xticks(rotation=0)
plt.tight_layout()

plt.bar(
    ['Movie', 'TV Show'],
    [6131, 2676],
    color=['#E50914', '#141414']
)


plt.savefig("netflix_content_distribution.png", dpi=300)
plt.show()

# Titles added by year and content type
titles_by_year = (
    df.dropna(subset=["year_added"])
    .groupby(["year_added", "type"])
    .size()
    .unstack(fill_value=0)
)

print("\nTitles added by year:")
print(titles_by_year)

titles_by_year.plot(
    kind="line",
    marker="o",
    figsize=(10, 6),
    color=["#E50914", "#141414"]
)

plt.title("Netflix Content Added Over Time")
plt.xlabel("Year Added")
plt.ylabel("Number of Titles Added")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    "netflix_content_over_time.png",
    dpi=300
)

plt.show()

# STEP 7 - Content growth visualization

titles_by_year.plot(
    kind="line",
    marker="o",
    figsize=(12, 6),
    color=["#E50914", "#141414"]
)

plt.title("Netflix Content Additions by Year")
plt.xlabel("Year Added")
plt.ylabel("Number of Titles")
plt.grid(alpha=0.3)
plt.legend(title="Content Type")
plt.tight_layout()

plt.savefig(
    "netflix_content_growth.png",
    dpi=300
)

plt.show()

# STEP 9 - Top 10 Countries Visualization

plt.figure(figsize=(12, 6))

top_countries.sort_values().plot(
    kind="barh",
    color="#E50914"
)

plt.title("Top 10 Countries by Netflix Titles")
plt.xlabel("Number of Titles")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig(
    "netflix_top_10_countries.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# STEP 10 - Genre Visualization

plt.figure(figsize=(12, 6))

top_genres.sort_values().plot(
    kind="barh",
    color="#E50914"
)

plt.title("Top 10 Netflix Content Categories")
plt.xlabel("Number of Titles")
plt.ylabel("Category")

plt.tight_layout()

plt.savefig(
    "netflix_top_genres.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# STEP 11 - Movies vs TV Shows

genre_comparison = (
    genre_df
    .groupby(["type", "listed_in"])
    .size()
    .reset_index(name="total")
)

# Top 5 categories for each content type
top_genres_by_type = (
    genre_comparison
    .sort_values(
        ["type", "total"],
        ascending=[True, False]
    )
    .groupby("type")
    .head(5)
)

print("\nTop 5 Categories by Content Type:")
print(top_genres_by_type)

# STEP 12 - Category Comparison Visualization

for content_type in ["Movie", "TV Show"]:

    data = top_genres_by_type[
        top_genres_by_type["type"] == content_type
    ]

    plt.figure(figsize=(10, 5))

    plt.barh(
        data["listed_in"],
        data["total"],
        color="#E50914"
    )

    plt.title(f"Top 5 Categories - {content_type}")
    plt.xlabel("Number of Titles")
    plt.ylabel("Category")

    plt.gca().invert_yaxis()

    plt.tight_layout()

    filename = content_type.lower().replace(" ", "_")

    plt.savefig(
        f"netflix_categories_{filename}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    # STEP 13 - Content Rating Analysis

rating_counts = (
    df[df["rating"] != "Unknown"]["rating"]
    .value_counts()
)

print("\nContent Rating Distribution:")
print(rating_counts)

# Percentage distribution
rating_percentage = (
    rating_counts / rating_counts.sum()
) * 100

print("\nRating Percentage:")
print(rating_percentage.round(2))

# STEP 13 - Rating Visualization

plt.figure(figsize=(12, 6))

rating_counts.sort_values().plot(
    kind="barh",
    color="#E50914"
)

plt.title("Netflix Content Rating Distribution")
plt.xlabel("Number of Titles")
plt.ylabel("Content Rating")

plt.tight_layout()

plt.savefig(
    "netflix_content_ratings.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# STEP 14 - Movie Duration Analysis

# Select only movies
movies_df = df[df["type"] == "Movie"].copy()

# Extract duration in minutes
movies_df["duration_minutes"] = pd.to_numeric(
    movies_df["duration"].str.extract(r"(\d+)\s*min")[0],
    errors="coerce"
)

# Descriptive statistics
print("\nMovie Duration Statistics:")
print(movies_df["duration_minutes"].describe())

# Check missing values
print("\nMissing movie durations:")
print(movies_df["duration_minutes"].isnull().sum())

# Investigate missing movie durations

print(
    movies_df[
        movies_df["duration_minutes"].isna()
    ][["title", "rating", "duration"]]
)

# Movie Duration Distribution

plt.figure(figsize=(12, 6))

plt.hist(
    movies_df["duration_minutes"],
    bins=30,
    color="red",
    edgecolor="black"
)

plt.title("Netflix Movie Duration Distribution")
plt.xlabel("Duration (minutes)")
plt.ylabel("Number of Movies")

plt.axvline(
    movies_df["duration_minutes"].mean(),
    color="blue",
    linestyle="--",
    label="Average Duration"
)
plt.savefig(
        f"netflix_movie_durations_{filename}.png",
        dpi=300,
        bbox_inches="tight"
)

plt.legend()
plt.tight_layout()
plt.show()

# TV Show Duration Analysis

tv_shows = df[df["type"] == "TV Show"].copy()

tv_shows["seasons"] = pd.to_numeric(
    tv_shows["duration"].str.extract(r"(\d+)")[0],
    errors="coerce"
)

print("\nTV Show Season Statistics:")
print(tv_shows["seasons"].describe())

print("\nTV Shows by Number of Seasons:")
print(tv_shows["seasons"].value_counts().sort_index())

plt.figure(figsize=(12, 6))

tv_shows["seasons"].value_counts().sort_index().plot(
    kind="bar",
    color="red",
    edgecolor="black"
)

plt.title("Netflix TV Shows by Number of Seasons")
plt.xlabel("Number of Seasons")
plt.ylabel("Number of TV Shows")

plt.savefig(
        f"netflix_tv_shows_seasons_{filename}.png",
        dpi=300,
        bbox_inches="tight"
)

plt.tight_layout()
plt.show()

# Content Distribution by Release Year

release_distribution = (
    df.groupby(["release_year", "type"])
    .size()
    .unstack(fill_value=0)
)

print("\nContent by Release Year:")
print(release_distribution.tail(20))

# Visualisation
plt.figure(figsize=(12, 6))

release_distribution.loc[2000:2021].plot(
    kind="line",
    marker="o",
    figsize=(12, 6),
    color=["#E50914", "#141414"]
)

plt.title("Netflix Content by Release Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")

plt.savefig(
        f"netflix_content_release_year_2000_2021_{filename}.png",
        dpi=300,
        bbox_inches="tight"
)

plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Save the cleaned dataset to a new CSV file
df.to_csv("netflix_titles_cleaned.csv", index=False)
print("\nClean dataset saved successfully!")