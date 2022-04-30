import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

/**
 * Build a model from a database of sentences to predict the best POS for words in a sentence
 * Supports both console and file driven usage
 *
 * @author Zachary Wong
 * Dartmouth CS10, Spring 2021
 */

public class POS {

    // instance variables for map counts
    HashMap<String, Integer> wordtoStateCount;
    HashMap<String, Integer> tagtoTagCount;
    HashMap<String, Integer> totalwordtoTagCount;
    HashMap<String, Integer> totaltagtoTagCount;

    // instance variables for map probabilities
    HashMap<String, Double> wordtoTagProbability;
    HashMap<String, Double> tagtoTagProbability;

    // instance variables for model
    HashMap<String, HashMap<String, ArrayList<String>>> wordtoState;

    // instance variable for Viterbi Table and list of Maps
    ArrayList<HashMap<String, HashMap<String, HashMap<String, Double>>>> viterbiList;
    HashMap<String, HashMap<String, HashMap<String, Double>>> viterbiTable;
    HashMap<String, Double> currentTagtoScoreMap;
    HashMap<String, HashMap<String, Double>> nextTagtoCurrentTagMap;


    // Map of all possible transitions
    HashMap<String, ArrayList<String>> tagTransitions = new HashMap<>();

    // tags for each word in a sentence
    ArrayList<String> taggedSentence;


    // unobserved probability score
    Double unobservedScore = -100.0;

    // key to track whether game needs to be quit
    String key = "";

    /**
     * Constructor for this class
     */
    public POS() {
        // the map counts
        wordtoStateCount = new HashMap<>();
        tagtoTagCount = new HashMap<>();
        totalwordtoTagCount = new HashMap<>();
        totaltagtoTagCount = new HashMap<>();

        // the map probabilities
        wordtoTagProbability = new HashMap<>();
        tagtoTagProbability = new HashMap<>();

        // the map model
        wordtoState = new HashMap<>();
    }

    /**
     * Helper Function
     * Update the total count for each tag based on words
     * @param tag the tag to be updated
     */
    public void wordtoTagTotalUpdate(String tag) {
        if (!totalwordtoTagCount.containsKey(tag)) {
            totalwordtoTagCount.put(tag, 1);
        } else {
            // add one
            totalwordtoTagCount.put(tag, (totalwordtoTagCount.get(tag) + 1));
        }
    }

    /**
     * Helper Function
     * Update the total count for each tag based on the transition number
     * @param tag the tag to be updated
     */
    public void statetoStateTotalUpdate(String tag) {
        // if the map does not contain the key
        if (!totaltagtoTagCount.containsKey(tag)) {
            totaltagtoTagCount.put(tag, 1);
        }
        // if the map contains the key already
        else {
            // add one
            totaltagtoTagCount.put(tag, (totaltagtoTagCount.get(tag) + 1));
        }
    }

    /**
     * populates the word to State map with counts
     * Also updates the total count of each state
     * @param wordInput the input of sentences
     * @param tagInput input of tags
     * @throws IOException exception
     */
    public void countWordtoState(BufferedReader wordInput, BufferedReader tagInput) throws IOException {

        // read and parse/change lower case
        String wordLine = wordInput.readLine();
        String tagLine = tagInput.readLine();
        String[] currentWord = wordLine.toLowerCase().split(" ");
        String[] currentTag = tagLine.split(" ");

        while (wordLine != null) {
            int i = 0;
            // for each word in the line
            while (i < currentWord.length) {

                // the case when the map does not have the word/tag pair yet
                if (!wordtoStateCount.containsKey(currentWord[i] + "==" + currentTag[i])) {
                    wordtoStateCount.put(currentWord[i] + "==" + currentTag[i], 1);
                }
                else {
                    // add one
                    wordtoStateCount.put(currentWord[i] + "==" + currentTag[i], (wordtoStateCount.get(currentWord[i] + "==" + currentTag[i])) + 1);
                }
                wordtoTagTotalUpdate(currentTag[i]);  //update total
                i++;
            }

            // read in the next line
            // break if the line is null and don't parse/change to lower case
            wordLine = wordInput.readLine();
            tagLine = tagInput.readLine();
            if (wordLine == null){
                break;
            }
            else
            {
                currentWord = wordLine.toLowerCase().split(" ");
                currentTag = tagLine.split(" ");
            }
        }
//        System.out.println("word to state count map: " + wordtoStateCount);
//        System.out.println("---------------" );
//        System.out.println("total word to state count map: " + totalwordtoTagCount);
//        System.out.println("---------------" );
        wordInput.close();
        tagInput.close();
    }

    /**
     * populates the state to State map with counts
     * @param tagInput input of tags
     * @throws IOException exception
     */
    public void counttagtoTag(BufferedReader tagInput) throws IOException {

        // read and parse lines
        String tagLine = tagInput.readLine();
        String[] currentTag = tagLine.split(" ");


        while (tagLine != null) {

            if (!tagtoTagCount.containsKey("#==" +  currentTag[0])) {
                tagtoTagCount.put("#==" +  currentTag[0], 1);
            }
            else {
                // add 1 to the count
                tagtoTagCount.put("#==" +  currentTag[0], (tagtoTagCount.get("#==" +  currentTag[0])) + 1);
            }
            statetoStateTotalUpdate("#");

            int i = 0;
            // for each word in the line
            while (i < (currentTag.length-1)) {
                // the case when the map does not have the word/tag pair yet
                if (!tagtoTagCount.containsKey(currentTag[i] + "==" + currentTag[i+1])) {
                    tagtoTagCount.put(currentTag[i] + "==" + currentTag[i+1], 1);
                }
                else {
                    // add 1 to the count
                    tagtoTagCount.put(currentTag[i] + "==" + currentTag[i+1], (tagtoTagCount.get(currentTag[i] + "==" + currentTag[i+1])) + 1);
                }
                statetoStateTotalUpdate(currentTag[i]); //update total
                i++;
            }

            // read in the next line
            // break if the line is null and don't parse
            tagLine = tagInput.readLine();
            if (tagLine == null){
                break;
            }
            else
            {
                currentTag = tagLine.split(" ");
            }
        }
        tagInput.close();
//        System.out.println("tag to tag count map: " + tagtoTagCount);
//        System.out.println("total tag to tag count map: " + totaltagtoTagCount);
//        System.out.println("---------------" );

    }

    /**
     * Populates map for each word and its probability of being a certain state
     */
    public void calculateprobabilitywordtoState(){
        Set<String> keys = wordtoStateCount.keySet();

        // for each key
        for(String key: keys){
            String[] state = key.split("==");    // get the tag of the word

            // divide the count over the total
            double value = Math.log((double) wordtoStateCount.get(key) / totalwordtoTagCount.get(state[1]));
            wordtoTagProbability.put(key, value);       //put in the map
        }
//        System.out.println("word as a tag probability map: " + wordtoTagProbability);
//        System.out.println("---------------" );


    }
    /**
     * Populates map for each word its probability
     */
    public void calculateprobabilitytagtoTag(){
        Set<String> keys = tagtoTagCount.keySet();

        // for every tag
        for(String key: keys){
            String[] state = key.split("==");        // get the start tag
//            System.out.println(tagtoTagCount.get(key));
//            System.out.println(totaltagtoTagCount.get(state[0]));

            // divide count over total
            double value = Math.log((double) tagtoTagCount.get(key) / totaltagtoTagCount.get(state[0]));
            tagtoTagProbability.put(key, value);        //put in the map

        }
//        System.out.println("tag to tag probability map: " + tagtoTagProbability);
//        System.out.println("---------------" );

    }

    /**
     * Helper function
     * create a library of all seen tag transitions
     */
    public void getAllPossibleTagTransitions(){

        // get all the possible tag transitions
        Set<String> tagTransitionsSet = tagtoTagCount.keySet();

        // for each transition, parse into an array
        for (String transition: tagTransitionsSet){
            String[] transitionParsed = transition.split("==");

            // put into the map with a new array list as value if not seen yet
            if (!tagTransitions.containsKey(transitionParsed[0])){
                tagTransitions.put(transitionParsed[0], new ArrayList<>());
                tagTransitions.get(transitionParsed[0]).add(transitionParsed[1]);
            }

            // get the list from the key and add the next state into the list
            else{
                tagTransitions.get(transitionParsed[0]).add(transitionParsed[1]);
            }

        }
//        System.out.println("all possible transitions " + tagTransitions);

    }

    /**
     * Helper function to update the inner map with types String, ArrayList<String>
     * @param word the current word (key of outer map)
     * @param tag the current tag (tag of the word)
     * @param nextTag the next tag to be added
     */
    public void updateInnerMap(String word, String tag, String nextTag){

        // if the tag of the word is already in the inner map, add the next tag to value (list) of the tag and if not
        // a duplicate tag/next tag pair
        if (wordtoState.get(word).containsKey(tag) && !wordtoState.get(word).get(tag).contains(nextTag)){
            wordtoState.get(word).get(tag).add(nextTag);
        }

        // if the tag of the word is not in the inner map, create a new array list, put the next tag into the list
        // and store as value of this inner map
        else if (!wordtoState.get(word).containsKey(tag))
        {
            ArrayList<String> nextTags = new ArrayList<>();
            nextTags.add(nextTag);
            wordtoState.get(word).put(tag, nextTags);
        }
    }

    /**
     * Creates the map wordtoState outer and inner maps to prepare for counts
     * Outermap key to value is (Word to another map)
     * Inner map key to value is (currentstate to nextstate)
     *
     * @param tagInput  the input of tags
     * @param wordInput the input of sentences
     */
    public void createModel(BufferedReader wordInput, BufferedReader tagInput) throws IOException {

        // read in the inputs and parse each one (lower case the words)
        String wordLine = wordInput.readLine();
        String tagLine = tagInput.readLine();
        String[] currentWord = wordLine.toLowerCase().split(" ");
        String[] currentTag = tagLine.split(" ");

        while (wordLine != null){
            int i = -1;

            // handle the start cases
            if (!wordtoState.containsKey("N/A")){
                HashMap<String, ArrayList<String>> statetoState = new HashMap<>();     // create new inner map and put as value
                wordtoState.put("N/A", statetoState);

                // create a new list for the inner map and add the next tag into the list and put the list as value of the
                // inner map
                ArrayList<String> nextTags = new ArrayList<>();
                nextTags.add(currentTag[0]);
                statetoState.put("#", nextTags);
                i++;
            }

            // handles the case if the word is already in the outermap and the inner map is already created
            else{
                updateInnerMap("N/A", "#", currentTag[0]);      // helper function to update the inner map
                i++;
            }

            // for each word in the line after the start case
            while (i < currentWord.length-1) {

                // the case when the map does not have the word yet
                if (!wordtoState.containsKey(currentWord[i])){
                    HashMap<String, ArrayList<String>> statetoState = new HashMap<>();     // create new inner map and put as value
                    wordtoState.put(currentWord[i], statetoState);

                    // create a new list for the inner map and add the next tag into the list and put the list as value of the
                    // inner map
                    ArrayList<String> nextTags = new ArrayList<>();
                    nextTags.add(currentTag[i+1]);
                    statetoState.put(currentTag[i], nextTags);
                    i++;
                }

                // handles the case if the word is already in the outermap and the inner map is already created
                else{
                    updateInnerMap(currentWord[i], currentTag[i], currentTag[i+1]); // helper function to update the inner map
                    i++;
                }

        }
            // read in the next line
            // break if the line is null and don't parse/change to lower case
            wordLine = wordInput.readLine();
            tagLine = tagInput.readLine();
            if (wordLine == null){
                break;
            }
            else
            {
                currentWord = wordLine.toLowerCase().split(" ");
                currentTag = tagLine.split(" ");
            }
        }

//        System.out.println("model word to State: " + wordtoState);
//        System.out.println("---------------" );

        wordInput.close();
        tagInput.close();
    }

//    /**
//     *
//     * @param observation
//     * @param partialMap
//     */
//    public void updateTable(String observation, HashMap<HashMap<String, String>, Double> partialMap){
//        viterbiTable = new HashMap<>();
//       viterbiTable.put(observation, partialMap);
//       viterbiList.add(viterbiTable);
//    }

    /**
     * Update the first row of the viterbi table with the # state and N/A as the word
     */
    public void updateFirstRow(){
        // create new viterbi table with corresponding inner maps
        currentTagtoScoreMap = new HashMap<>();
        nextTagtoCurrentTagMap = new HashMap<>();
        viterbiTable = new HashMap<>();

        // populate the maps with custom inputs (observation is N/A and next tag is #)
        currentTagtoScoreMap.put("0", 0.0);
        nextTagtoCurrentTagMap.put("#", currentTagtoScoreMap);
        viterbiTable.put("N/A", nextTagtoCurrentTagMap);
        viterbiList.add(viterbiTable);
    }

    /**
     * Helper function to get the score
     * @param currentState the current state
     * @param nextState the next state for the observation
     * @param observation the observation
     * @param previousObservation the previous observation
     * @return the score
     */
    public Double getScore(String currentState, String nextState, String observation, String previousObservation){
        double result;
        double observationProbability;

        //takes care of unobserved probability of word as a tag
        if (wordtoTagProbability.get(observation + "==" + nextState) == null){
            observationProbability = unobservedScore;
        }
        else{
           observationProbability = wordtoTagProbability.get(observation + "==" + nextState);
        }

        // get the current score (get from the last observation with corresponding current tags)
        Set<String> currentStates = viterbiList.get(viterbiList.size()-1).get(previousObservation).get(currentState).keySet();
        double currentScore = 0;
        for(String state: currentStates){
            currentScore = viterbiList.get(viterbiList.size()-1).get(previousObservation).get(currentState).get(state);
        }

        // get the probability of transition from the current to next state
        double transitionProbability = tagtoTagProbability.get(currentState + "==" + nextState);

        // add the three probabilities and return
        result = observationProbability + currentScore + transitionProbability;
        return result;

    }


    /**
     * Builds the table and list of tables and returns the tagged sentence
     * @param currentSentence the sentence to be tagged
     */
    public ArrayList<String> createTableandTagWords(String currentSentence) {

        // create the new list and update first row
        viterbiList = new ArrayList<>();
        updateFirstRow();


        // put N/A as first word and put all observations in sentence in array list
        String[] sentence = currentSentence.toLowerCase().split(" ");
        ArrayList<String> sentenceList = new ArrayList<>();
        for (String word : sentence) {
            sentenceList.add(word);
        }
        sentenceList.add(0, "N/A");


        // start from index 1
        int observationIndex = 1;
        while (observationIndex < sentenceList.size()) {

            // create the table and first inner map
            nextTagtoCurrentTagMap = new HashMap<>();
            viterbiTable = new HashMap<>();


            String previousObservation = sentenceList.get(observationIndex - 1);    // previous observation

            // put all current possible states in a set
            Set<String> allCurrentStates = viterbiList.get(viterbiList.size() - 1).get(previousObservation).keySet();

            // search up all possible next states in the library from the current state
            for (String currentState : allCurrentStates) {

                //search up in library
                ArrayList<String> nextStates = (tagTransitions.get(currentState));
                String observation = sentenceList.get(observationIndex);

                // for each next states for a current state, put in map with score
                if (nextStates != null){
                    for (String nextstate : nextStates) {
                        currentTagtoScoreMap = new HashMap<>();

                        // get the score
                        double score = getScore(currentState, nextstate, observation, previousObservation);

                        // check if the next state is already in the map for the observation and keep the bigger next state-current state combination
                        if (viterbiTable.size() > 0) {
                            if (viterbiTable.get(observation).containsKey(nextstate)) {

                                //get the score of the row with the same next state
                                Set<String> currentstatesforduplicatenextStates = viterbiTable.get(observation).get(nextstate).keySet();
                                double duplicatenextStateScore;

                                // for each of the duplicate next states for the observation, get the score
                                for (String currentStateforDuplicatenextState : currentstatesforduplicatenextStates) {
                                    duplicatenextStateScore = viterbiTable.get(observation).get(nextstate).get(currentStateforDuplicatenextState);

                                    // if the current score is bigger, then remove the previous row and replace it with the current row of tags and scores
                                    if (score > duplicatenextStateScore) {
                                        viterbiTable.get(observation).remove(nextstate);
                                        currentTagtoScoreMap.put(currentState, score);
                                        nextTagtoCurrentTagMap.put(nextstate, currentTagtoScoreMap);
                                        viterbiTable.put(observation, nextTagtoCurrentTagMap);
                                    }
                                }
                            }
                            // if the first word in the sentence
                            else
                            {
                                currentTagtoScoreMap.put(currentState, score);
                                nextTagtoCurrentTagMap.put(nextstate, currentTagtoScoreMap);
                                viterbiTable.put(observation, nextTagtoCurrentTagMap);
                            }
                        }
                        // if the table does not have the duplicate next state
                        else
                        {
                            currentTagtoScoreMap.put(currentState, score);
                            nextTagtoCurrentTagMap.put(nextstate, currentTagtoScoreMap);
                            viterbiTable.put(observation, nextTagtoCurrentTagMap);
                        }

                    }
                }
            }

            // add the table to the list when done and move on to the next word
            viterbiList.add(viterbiTable);
            observationIndex++;
        }
//        System.out.println(viterbiList);
        return tagWords(sentenceList);      // helper function called
    }


    /**
     * Helper function to tag the words based on the viterbitables
     * @param sentenceList the sentence (in array form) to be tagged
     */
    public ArrayList<String> tagWords(ArrayList<String> sentenceList){
        // create a new Arraylist for each sentence
        taggedSentence = new ArrayList<>();

        // get the last observation and last tags and put into the head of the tagged sentence
        String lastObservation = sentenceList.get(sentenceList.size()-1);
        String lastTag = keepBestScore(lastObservation, viterbiList.get(viterbiList.size()-1));     // call helper function
        taggedSentence.add(0,  lastTag);

        // decremeent the index keeping count of the sentence and viterbi table in the list
        int viterbiIndex = viterbiList.size()-1;
        int observationIndex = sentenceList.size()-1;

        // for each, get the current state and put as the state for the previous observation
        while(viterbiIndex > 1){
            Set<String> currentState = viterbiList.get(viterbiIndex).get(sentenceList.get(observationIndex)).get(taggedSentence.get(0)).keySet();
            for(String state: currentState){
                taggedSentence.add(0, state);
            }
            viterbiIndex--;
            observationIndex--;
        }

        // nicer output form that adds the word to the tag in the output
        observationIndex = sentenceList.size()-1;
        int taggedIndex = taggedSentence.size()-1;

        // replaces the current element with the upgraded word/tag format
        while(observationIndex > 0){
            taggedSentence.add(taggedIndex, sentenceList.get(observationIndex) + "/" + taggedSentence.get(taggedIndex));
            taggedSentence.remove(taggedIndex + 1);
            observationIndex--;
            taggedIndex--;
        }
//        System.out.println("Current Tagged Sentence: " + taggedSentence);
        return taggedSentence;      // return


        // get the current state from fish
        // put in tagged Sentence as next previous word
        // continue until


    }

    /**
     * Helper function
     * get the best score from the last observation of the sentence
     * @param lastObservation the last word of the sentence
     * @param lastTable the corresponding table for the last word of the sentence
     * @return the tag of the last word
     */
    public String keepBestScore(String lastObservation, HashMap<String, HashMap<String, HashMap<String, Double>>> lastTable){

        // for each next state of observation
        // get score and switch out if lower than the previous

        // initialize best score as negative infinity and state and null
        double bestScore = Double.NEGATIVE_INFINITY;
        String bestState = null;

        // get all next states of the last word
        Set<String> nextStates = lastTable.get(lastObservation).keySet();

        // for each next state of the last word
        for (String nextState: nextStates){
            Set<String> currentStates = lastTable.get(lastObservation).get(nextState).keySet();

            // for each current state of the last word
            for(String currentState: currentStates){

                // get the best score and update the best state accordingly
                double currentScore = lastTable.get(lastObservation).get(nextState).get(currentState);
                if(currentScore > bestScore){
                    bestScore = currentScore;
                    bestState = nextState;
                }
            }

        }
        return bestState;   // return the best tag for the last word

    }

    /**
     * This method tags the entire file
     * @param input the input of new sentences to tag
     * @return the string of tagged sentneces
     * @throws IOException exception
     */
    public String tagEntireFile(BufferedReader input) throws IOException {
        //read in the line

        // ouput each one of them
        String result = "";
        String line = input.readLine();
        while(line != null){
        // tag each sentence and append to the result string
          ArrayList<String> taggedSentence = createTableandTagWords(line);
          for (int i = 0; i < taggedSentence.size(); i++){
              // copy tagged sentence out of array list and into the entire result string
              result = result + " " + taggedSentence.get(i);
          }
            result += "\n";
            line = input.readLine();
        }
        input.close();
        return result;
    }

    /**
     * Helper function to run the methods to create the model for file-driven usage
     * @param sentenceFilePathName the path name to the training sentence file
     * @param tagFilePathName the path name to the training tag file
     * @throws IOException exception for file read
     */
    public void run(String sentenceFilePathName, String tagFilePathName) throws IOException {

        countWordtoState(new BufferedReader(new FileReader(sentenceFilePathName)), new BufferedReader(new FileReader(tagFilePathName)));
        counttagtoTag(new BufferedReader(new FileReader(tagFilePathName)));
        calculateprobabilitywordtoState();
        calculateprobabilitytagtoTag();
        getAllPossibleTagTransitions();
        createModel(new BufferedReader(new FileReader(sentenceFilePathName)), new BufferedReader(new FileReader(tagFilePathName)));
        //tagEntireFile(new BufferedReader(new FileReader(se)));
    }

    /**
     * The interactive console-driven usage
     * @return the string with words tagged in "word/tag" format
     */
    public String interactive(){
        Scanner in = new Scanner(System.in);        // creates scanner

        // instructions to user
        System.out.println("Type a sentence");
        System.out.println("Type q to quit");
        String sentence = in.nextLine();
        String result = "";

        // create the table and tag the words for the line
        ArrayList<String> taggedSentence = createTableandTagWords(sentence);

            // for each tagged line, append to the empty string
            for (int i = 0; i < taggedSentence.size(); i++){
                // copy tagged sentence out of array list and into the entire result string
                result = result + " " + taggedSentence.get(i);
            }
            result += "\n";

        //take care of quitting the game (when q is pressed)
        key = sentence;
        if (key.equals("q")){
            return result;      // return the string
        }
        else{
            return result;      // return the string
        }
    }

    /**
     * runs the interactive method
     */
    public void runInteractive(){
        // keep running until the user enters q
        while (!key.equals("q")){
            System.out.println(interactive());
        }
    }

    /**
     * Run
     * @param args run
     * @throws IOException exception for file not being found
     */
    public static void main(String[] args) throws IOException {

        // example test
//        POS test0 = new POS();
//        test0.run("input/patterntexts/example-sentences.txt", "input/patterntexts/example-tags.txt");
//        System.out.println(test0.tagEntireFile(new BufferedReader(new FileReader("input/patterntexts/example-sentences.txt"))));

        // simple train test
//        POS test1 = new POS();
//        test1.run("input/patterntexts/simple-train-sentences.txt", "input/patterntexts/simple-train-tags.txt");
//        System.out.println(test1.tagEntireFile(new BufferedReader(new FileReader("input/patterntexts/simple-test-sentences.txt"))));

        // brown test and console-driven testing based on model by brown training  sentences
        POS test2 = new POS();
        test2.run("patterntexts/brown-train-sentences.txt", "patterntexts/brown-train-tags.txt");
        System.out.println(test2.tagEntireFile(new BufferedReader(new FileReader("patterntexts/brown-test-sentences.txt"))));
        test2.runInteractive();

    }
}
