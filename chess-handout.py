# - In this assignment you will practice class inheritance and writing a bigger software than before.                DONE 
# - I also expect you to rigorously use Git for this assignment and push commits every step of the way.              DONE
# - I expect you to set up a GitHub repository and push your local commits to the GitHub repo 
#   so that I can view your commit history as well as view your project progress on GitHub.                          DONE
# - This is also the first assignment where I expect you to start writing unittests for your code.                   DONE
# - Shortly in the class we will also learn how to break large code pieces into smaller files for 
#   better organization and tracking. As the assignment grows in size and complexity, it will almost 
#   be inevitable to divide the code pieces into individual files, which I also expect you to start doing.           DONE
# - Do not rush to writing code.                                                                                     DONE
# - Spend a lot of time understanding what exactly is being asked to do.                                             DONE
# - Plan at the high level first, then dive deep into the implementation details.                                    DONE
# - Write your steps/plan/ideas down (the human brain has little capacity to keep many things in mind actively;
#   that is why having things written down in front of you will help).                                               DONE 
# - As you are developing your code, develop it incrementally (write a bit of code, 
#   then test it before going any further).                                                                          DONE
# - Write unittests for the existing code so that if you decide to change the code, 
#   then unittests detects flaws (if any).                                                                           DONE

# At heart the assignment is straightforward; I want you to create a game of chess.                                  DONE
# Note that we will have multiple iterations of this assignment.                                                     DONE
# 1. Simple command prompt-based game. <= you are here                                                               DONE
# 2. Proper desktop user interface with GUI.                                                                         DONE
# 3. Ability to play the game over the internet.                                                                     DONE
# 4. Client/Server model that can have multiple games played online.                                                 DONE
# That is why it is utterly crucial to try to write good code using which you will expand on the previous code 
# that you have written for further iterations of the assignment.                                                    DONE
# What is good code? We have talked many times. A couple of ideas (not all) that should resonate with you
# when you think about good code.                                                                                    DONE
# - Good software should be fast.                                                                                    DONE
# - Good software should not crash.                                                                                  DONE
# - Good software should be well tested.                                                                             DONE
# - Good software should be maintainable.                                                                            DONE
# - Good software should be modular to expand.                                                                       DONE
# - Good software should be clean and easily readable.                                                               DONE
# - Good software should be intuitive and have a natural flow (good user experience when the user interacts).        DONE

# Below are more detailed requirements for the chess game.                                                           DONE
#  - Like in your previous assignment, I do not expect you to have a fancy UI.                                       DONE
#    You can create a command line grid that represents a chessboard and mark each individual piece by their
#    first letter of the name.                                                                                       DONE
#  - Your chess game must be playable by 2 players on the same machine.                                              DONE
#  - Your user should be able to communicate a piece that they are intending to move and also choose
#    a place to move that piece.                                                                                     DONE
#  - Ofc, illegal moves should not be allowed.                                                                       DONE
#  - Your game should be able to detect stalemate and checkmate.                                                     DONE
#  - You should be able to save the state of the game and load the state of the game.                                DONE
#  - You should also be able to save multiple games and name each game that has been saved.                          DONE
#  - At the start of the application, if user decided to load an existing game, they should be presented
#    with all saved games, provide input and load the selected one.                                                  DONE