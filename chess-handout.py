# - In this assignment you will practice class inheritance and writing a bigger software than before.                DONE 
# - I also expect you to rigorously use Git for this assignment and push commits every step of the way.              DONE





# - I expect you to setup a Github repository and push your local commits to the Github repo so 
#   that i can view your commit history as well as view your project progress on Github.
# - This is also the first assignment where I expect you to start writing unittests for your code.
# - Shortly in the class we will also learn how to break large code piece into smaller files for
#   better organization and tracking. As the assignment growth in size and complexity, it will almost
#   be inevitable to divide the code pieces into individual files, which i also expect you to start doing.
# - Spend a lot of time understanding what is exactly being asked to do.
# - Do not rush to writing code.
# - Plan at the high level first then dive deep into the implementation details.
# - Write your steps/plan/ideas down (human brain has little capacity to keep many things in mind actievely, that is why having things
#   written down in front of you will help).
# - As you are developing your code, develop it incrementally (write a bit of code then test it before going any further).
#   - Write unittests for the existing code so that if you decide to change the code, then unittests detects flaws (if any)


# At the heart the assignment is straight forward, I want you to create a game of chess.
# Note that we will have multiple iterations of this assignment.
# 1. Simple command prompt based game. <= you are here
# 2. Proper desktop user interface with GUI.
# 3. Ability to play the game over the internet.
# 4. Client/Server model that can have multiple games played online.
# That is why it is utterly crucial to try to write a good code using which you will expand on the
# previous code that you have written for further iterations of the assignment.
# What is good code we have talked many times. Couple of ideas (not all) that should ressonate with you
# when you think about good code.
# - Good software should be clean and easily readable.
# - Good software should be maintainable.
# - Good software should be modular to expand.
# - Good software should not crash.
# - Good software should be well tested.
# - Good software should be fast.
# - Good software should be inuitive and have a natural flow (good user experience when user interacts).


# Below are more detailed requirements for the chess game.
#  - Like in your previous assignment, I do not expect you to have a fancy UI. 
#    You can create a command line grid that represents a chess board and mark each individual piece by their
#    first letter of the name.
#  - You chess game must be playable by 2 players on the same machine.
#  - Your user should be able to communicate a piece that they are intending to move and also choose
#    a place to move that piece.
#  - Ofc, illegal moves should not be allowed.
#  - Your game should be able to detect stalemate, checkmate.
#  - You should be able to save the state of the game and load the state of the game.
#  - You should also be able to save multiple games and name each game that has been saved.
#  - At the start of the application, if user decided to load an existing game, they should be presented
#    with all saved games, provide input and load the selected one.