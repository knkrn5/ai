import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("data/game_data.csv")

# Display the data for initial reference
print("Initial Data:\n", df)

# Menu loop
while True:
    print("\nMENU:")
    print("1. Add a new column")
    print("2. Add a new row")
    print("3. Indexing")
    print("4. Print first 5 records (head)")
    print("5. Print last 3 records (tail)")
    print("6. Show the shape of the DataFrame")
    print("7. Show the size of the DataFrame")
    print("8. Show a histogram of the prices of games")
    print("9. Show a bar graph of the prices of games")
    print("10. Show games with a price below 20")
    print("11. Drop a specific column")
    print("12. Show grid on the plot")
    print("13. Add a legend to the plot")
    print("Enter any other number to EXIT")
    
    # Take user input with error handling
    try:
        choice = int(input("Enter your choice (1-13): "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 13.")
        continue

    if choice == 1:
        # Add a new column with some data
        # Check the number of rows in the DataFrame
        num_rows = len(df)

        # Create the 'Manufacturer' column with a matching length using repetition if necessary
        manufacturers = ['Nintendo', 'Nintendo', 'CD Projekt', 'Innersloth', 'Mojang', 'CD Projekt',
                        'Epic Games', 'Activision', 'Rockstar Games', 'Nintendo', 'Rockstar Games',
                        'Supergiant Games', 'Riot Games', 'Sucker Punch', 'ConcernedApe',
                        'Respawn', 'Riot Games', 'Ubisoft', 'Team Cherry', 'Square Enix']

        # Adjust the length of manufacturers to match the DataFrame's row count
        df['Manufacturer'] = (manufacturers * ((num_rows // len(manufacturers)) + 1))[:num_rows]

        print("\nUpdated Data with 'Manufacturer' column:\n", df)

        
    elif choice == 2:
        # Add a new row with sample data
        new_row = {
            'Game Name': 'New Game',
            'Developer': 'New Developer',
            'Price': 999.99,
            'Release Date': '2023-01-01',
            'Genre': 'Action',
            'Manufacturer': 'New Publisher'
        }

        # Convert the new row into a DataFrame
        new_row_df = pd.DataFrame([new_row])

        # Use pd.concat() to add the new row
        df = pd.concat([df, new_row_df], ignore_index=True)

        print("\nNew Row Added:\n", df.tail(1)) 
        
    elif choice == 3:
        # Example of indexing
        print("\nIndexing: Displaying the first 2 rows:\n", df.iloc[:2])
        
    elif choice == 4:
        # Print first 5 records (head)
        print("\nFirst 5 Records (Head):\n", df.head())
        
    elif choice == 5:
        # Print last 3 records (tail)
        print("\nLast 3 Records (Tail):\n", df.tail(3))
        
    elif choice == 6:
        # Show the shape of the DataFrame (rows, columns)
        print("\nShape of the DataFrame (rows, columns):\n", df.shape)
        
    elif choice == 7:
        # Show the size of the DataFrame (number of elements)
        print("\nSize of the DataFrame (total elements):\n", df.size)
        
    elif choice == 8:
        # Show a histogram of the prices of games
        plt.figure(figsize=(10,6))
        plt.hist(df['Price'], bins=10, color='skyblue', edgecolor='black')
        plt.xlabel('Price (INR)')
        plt.ylabel('Frequency')
        plt.title('Histogram of Game Prices')
        plt.show()
        print("Histogram of Game Prices displayed.")
        
    elif choice == 9:
        # Show a bar graph of the prices of games
        plt.figure(figsize=(10,6))
        plt.bar(df['Game Name'], df['Price'], color='skyblue')

        # Add labels and title
        plt.xlabel('Game Name')
        plt.ylabel('Price (INR)')
        plt.title('Price of Games')

        # Rotate the x-axis labels to make them readable
        plt.xticks(rotation=90)

        # Show the plot
        plt.tight_layout()
        plt.show()
        
    elif choice == 10:
        # Show games with a price below 20
        print("\nGames with Price Below ₹20:\n", df[df['Price'] < 20])
        
    elif choice == 11:
        # Drop a specific column
        column_to_drop = input("Enter the column name you want to drop: ")
        if column_to_drop in df.columns:
            df.drop(columns=[column_to_drop], inplace=True)
            print(f"\n'{column_to_drop}' column has been dropped.")
            print("\nUpdated Data:\n", df)
        else:
            print("Column not found. Please enter a valid column name.")
        
    elif choice == 12:
        # Show grid on the plot
        plt.figure(figsize=(10,6))
        plt.bar(df['Game Name'], df['Price'], color='skyblue')
        plt.xlabel('Game Name')
        plt.ylabel('Price (INR)')
        plt.title('Price of Games')
        plt.xticks(rotation=90)
        plt.grid(True)  # Enable grid
        plt.tight_layout()
        plt.show()
        print("Bar graph with grid displayed.")
        
    elif choice == 13:
        # Add a legend to the plot
        plt.figure(figsize=(10,6))
        plt.bar(df['Game Name'], df['Price'], color='skyblue', label="Game Prices")
        plt.xlabel('Game Name')
        plt.ylabel('Price (INR)')
        plt.title('Price of Games')
        plt.xticks(rotation=90)
        plt.legend()  # Add legend
        plt.tight_layout()
        plt.show()
        print("Bar graph with legend displayed.")
        
    else:
        print("Exiting...")
        break
