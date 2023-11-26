from openai import OpenAI
import os
import json
import random

philosophical_concepts = [
    "Existentialism", "Determinism", "Dualism", "Monism", "Nihilism", 
    "Realism", "Idealism", "Empiricism", "Rationalism", "Skepticism",
    "Pragmatism", "Stoicism", "Humanism", "Absurdism", "Relativism",
    "Solipsism", "Utilitarianism", "Hedonism", "Altruism", "Egoism",
    "Materialism", "Phenomenology", "Deontology", "Aesthetics", "Objectivism",
    "Subjectivism", "Empathy", "Ethnocentrism", "Holism", "Individualism",
    "Collectivism", "Romanticism", "Enlightenment", "Metaphysics", "Epistemology",
    "Ontology", "Teleology", "Theism", "Atheism", "Agnosticism",
    "Pantheism", "Fatalism", "Anarchism", "Marxism", "Capitalism",
    "Socialism", "Libertarianism", "Nationalism", "Globalism", "Pluralism",
    "Secularism", "Dogmatism", "Relativism", "Absolutism", "Mysticism",
    "Transcendentalism", "Pacifism", "Asceticism", "Autonomy", "Causality",
    "Vitalism", "Pessimism", "Optimism", "Empiricism", "Rationality",
    "Intuitionism", "Naturalism", "Essentialism", "Perfectionism", "Nativism",
    "Progressivism", "Conservatism", "Skepticism", "Traditionalism", "Postmodernism",
    "Structuralism", "Functionalism", "Behaviorism", "Positivism", "Constructivism",
    "Ecofeminism", "Egalitarianism", "Meritocracy", "Totalitarianism", "Authoritarianism",
    "Democracy", "Aristocracy", "Oligarchy", "Platonism", "Socratic",
    "Nietzscheanism", "Kantianism", "Hegelianism", "Darwinism", "Freudianism",
    "Confucianism", "Taoism", "Buddhism", "Stoicism", "Cynicism"
]


poets = [
    "T.S. Eliot", "Robert Frost", "Sylvia Plath", "Langston Hughes", "Maya Angelou",
    "Pablo Neruda", "Seamus Heaney", "W.H. Auden", "Ezra Pound", "Ted Hughes",
    "Allen Ginsberg", "Rumi", "Derek Walcott", "Rita Dove", "Adrienne Rich",
    "Philip Larkin", "Anne Sexton", "Elizabeth Bishop", "John Ashbery", "Billy Collins",
    "Carol Ann Duffy", "Mary Oliver", "Sharon Olds", "Charles Bukowski", "Audre Lorde",
    "Czesław Miłosz", "Octavio Paz", "Dylan Thomas", "Wallace Stevens", "Robert Hayden",
    "Gwendolyn Brooks", "Seamus Heaney", "E.E. Cummings", "Robert Lowell", "Wisława Szymborska",
    "Gulzar", "Amrita Pritam", "Kamala Das", "Agha Shahid Ali", "John Berryman",
    "Nikki Giovanni", "Simon Armitage", "Tracy K. Smith", "Joy Harjo", "Louise Glück",
    "Ocean Vuong", "Yusef Komunyakaa", "Saeed Jones", "Dorianne Laux", "Natalie Diaz"
]


styles = [
    "Modernism", "Postmodernism", "Surrealism", "Harlem Renaissance", "Beat Poetry",
    "Confessional Poetry", "New Criticism", "Black Mountain Poetry", "Language Poetry", "Imagism",
    "Futurism", "Dadaism", "Symbolism", "Vorticism", "Objectivism",
    "Flarf Poetry", "Conceptual Poetry", "New Formalism", "Ecopoetry", "Feminist Poetry",
    "Digital Poetry", "Spoken Word", "Performance Poetry", "Hip Hop Poetry", "Concrete Poetry",
    "Romanticism", "Expressionism", "Acmeism", "Futurism", "Suprematism",
    "Minimalism", "Dirty Realism", "Narrative Poetry", "L=A=N=G=U=A=G=E Poetry", "New York School",
    "Black Arts Movement", "Martian Poetry", "Deep Image Poetry", "Neo-Romanticism", "Avant-Garde Poetry",
    "Free Verse", "Prose Poetry", "Visual Poetry", "Sound Poetry", "Cyberpoetry",
    "Instapoetry", "Neoclassical Poetry", "Postcolonial Poetry", "Concrete Poetry", "Fluxus"
]

poetic_structures = [
    "Free Verse", "Haiku", "Sonnet", "Villanelle", "Sestina",
    "Limerick", "Ode", "Ghazal", "Tanka", "Ballad",
    "Blank Verse", "Rondeau", "Pantoum", "Acrostic", "Cinquain",
    "Epigram", "Concrete Poetry", "Elegy", "Narrative Poetry", "Lyric Poetry",
    "Prose Poetry", "Terza Rima", "Spoken Word", "Visual Poetry", "Ekphrastic Poetry"
]

literature_purposes = [
    "Satire", "Spiritual Enlightenment", "Entertainment", "Education", "Cultural Commentary",
    "Moral Instruction", "Historical Record", "Therapeutic Expression", "Social Critique", "Political Commentary",
    "Psychological Exploration", "Philosophical Inquiry", "Artistic Expression", "Romantic Escapism", "Horror and Suspense",
    "Mystery and Intrigue", "Science Fiction and Speculation", "Fantasy and World-Building", "Humor and Comedy", "Tragedy and Melodrama",
    "Biographical Accounts", "Autobiographical Reflection", "Creative Experimentation", "Language Preservation", "Myth and Folklore Creation"
]


client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv('OPENAI_API_KEY'),
)

def save_response_to_json(response, selected_concepts, selected_purpose, selected_structure, selected_style, filename='response.json', archive_filename='archive.json'):
    if response and response.choices:
        # Access the content attribute of the message object
        response_content = response.choices[0].message.content.strip()
        
        # Save to the individual file
        with open(filename, 'w') as json_file:
            json.dump({"message": response_content, "concepts": selected_concepts, "purpose": selected_purpose, "structure": selected_structure, "style": selected_style}, json_file)

        # Update the archive file
        try:
            # Read existing poems from the archive
            with open(archive_filename, 'r') as archive_file:
                archive_data = json.load(archive_file)
        except FileNotFoundError:
            # If the archive file doesn't exist, start with an empty list
            archive_data = []

        # Append the new poem to the archive
        archive_data.append({"message": response_content})

        # Save the updated archive
        with open(archive_filename, 'w') as archive_file:
            json.dump(archive_data, archive_file)



def fetch_chatgpt_response(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4",
        )
        return chat_completion
    except Exception as e:
        print(f"Error in fetching response: {e}")
        return None





def main():

    n = 1
    selected_concepts = random.sample(philosophical_concepts, n)
    selected_purpose = random.choice(literature_purposes)
    selected_structure = random.choice(poetic_structures)
    selected_style	 = random.choice(poets)
    poem_prompt = "you are a talented poet writing for " + selected_purpose + ". Without using these words, write a " + selected_structure + ", no more than 20 words long, about " + " and/or ".join(selected_concepts) + " in the style of " + selected_style + " with a one line title at the top." 





    print (poem_prompt)
    response = fetch_chatgpt_response(poem_prompt)
    if response:
        save_response_to_json(response, selected_concepts, selected_purpose, selected_structure, selected_style)

if __name__ == "__main__":
    main()
