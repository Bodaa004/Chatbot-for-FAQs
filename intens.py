import pandas as pd
import json

# Function to load and preprocess data
def load_and_preprocess_data(filepath):
    # Load data
    df = pd.read_csv(filepath)
    # Drop unwanted columns
    df.drop(columns=['isbn13', 'isbn10', 'subtitle', 'thumbnail'], inplace=True)
    return df

# Function to get book details by genre
def get_books_by_genre(df, genres, num_books=10):
    titles, authors, descriptions, rates = [], [], [], []

    for genre in genres:
        genre_data = df[df['categories'] == genre]
        # Ensure there are enough books in the genre
        if len(genre_data) < num_books:
            continue
        titles.append(genre_data['title'].values[:num_books])
        authors.append(genre_data['authors'].values[:num_books])
        # descriptions.append(genre_data['description'].values[:num_books])
        rates.append(genre_data['average_rating'].values[:num_books])

    return titles, authors, descriptions, rates

# Function to create intents
def create_intents(genres, titles, authors, descriptions, rates):
    intents = []

    for i, genre in enumerate(genres):
        responses = []
        for j in range(len(titles[i])):
            responses.append({
                "Book": titles[i][j],
                "Authors": authors[i][j],
                # "Feedback": descriptions[i][j],
                "Rate": rates[i][j]
            })

        intent = {
            "tag": genre,
            "patterns": [genre,f"Recommend a {genre} book",f"Recommend a book in {genre}"],
            "responses": responses
        }

        intents.append(intent)

    return intents

# Function to save intents to JSON
def save_intents_to_json(intents, output_filepath):
    data = {'intents': intents}
    with open(output_filepath, "w") as outfile:
        json.dump(data, outfile, indent=4)

# Main execution
if __name__ == "__main__":
    # Define filepaths
    data_filepath = 'data.csv'
    output_filepath = 'intents2.json'

    # Define genres
    genres = [
        'Fiction', 'Juvenile Fiction', 'Biography & Autobiography', 'History', 'Literary Criticism', 'Philosophy', 'Comics & Graphic Novels', 'Religion',
        'Drama', 'Juvenile Nonfiction', 'Poetry', 'Science', 'Literary Collections', 'Business & Economics', 'Social Science', 'Performing Arts', 'Cooking',
        'Art', 'Body, Mind & Spirit', 'Travel', 'Psychology', 'Computers', 'Self-Help', 'Political Science', 'Family & Relationships', 'Language Arts & Disciplines',
        'Humor', 'Health & Fitness', "Children's stories", 'Education', 'Medical', 'Nature', 'Adventure stories', 'Games', 'English fiction', 'Music', 'Sports & Recreation',
        'Detective and mystery stories', 'Fantasy fiction', 'American fiction', 'True Crime', 'Foreign Language Study', 'Science fiction', 'Law', 'Young Adult Fiction',
        'Photography', 'Architecture'
    ]

    # Load and preprocess data
    df = load_and_preprocess_data(data_filepath)

    # Get book details by genre
    titles, authors, descriptions, rates = get_books_by_genre(df, genres)

    # Create intents
    intents = create_intents(genres, titles, authors, descriptions, rates)

    # Save intents to JSON
    save_intents_to_json(intents, output_filepath)

print(f'Intenses completed. file saved to {output_filepath}')
