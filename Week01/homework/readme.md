# Exercise
1. create a folder and insert the three files "input.txt", "mapper.py", "reducer.py" into the folder.

2. Run the command below inside the folder (1)
   
docker run -it -p 9870:9870 -p 8088:8088 -v .:/app eecsyorku/eecs4415

4. Run the command below to insert input.txt file 

hdfs dfs -put ./input.txt /

5. Run the hadoop command below to perform the computation

    hadoop jar /usr/hadoop-3.0.0/share/hadoop/tools/lib/hadoop-streaming-3.0.0.jar \
    -file ./mapper.py \
    -mapper "python mapper.py" \
    -file ./reducer.py \
    -reducer "python reducer.py" \
    -input /input.txt \
    -output /output

5. Show the results by running the command below 

   hdfs dfs -cat /output/*

--- Result ---
E.g., the result
 
$418    1

1.5     1

Association     1

Here’s  1

In      1

It’s    1

Kevin   1

# Homework
1. Modify the exercise above so that it can read the Harry Potter book (sorcerers-stone.txt), and display the top 5 most frequent words (excluding stop words such as “a,” “an,” and “the”).
