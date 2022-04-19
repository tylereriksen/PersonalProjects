import java.util.Random;
import java.util.ArrayList;
import java.util.List;

class Coin {
    int identifier;
    double weight;

    Coin(int identifier, double weight) {
        this.identifier = identifier;
        this.weight = weight;
    }

    int getIdentifier() {
        return this.identifier;
    }

    double getWeight() {
        return this.weight;
    }
}

public class CounterfeitCoin {

    public static double getTotalWeight(ArrayList<Coin> listCoin) {
        double totalWeight = 0;
        for(Coin coin: listCoin) {
            totalWeight += coin.getWeight();
        }
        return totalWeight;
    }

    public static void main(String[] args) {
        int NUMCOINS = Integer.parseInt(args[0]);
        int COUNTERFEIT_ID = Integer.parseInt(args[1]);
        if(COUNTERFEIT_ID > NUMCOINS) {
            throw new IllegalArgumentException("Counterfeit Coin ID is not vallid.");
        }
        double REAL_WEIGHT = 1;
        double FAKE_WEIGHT = 0.5;
        int EXPECTED_TRIALS = (int)(Math.log(NUMCOINS - 0.5) / Math.log(3)) + 1;
        
        ArrayList<Coin> listCoin = new ArrayList<>();
        for(int i = 0; i < NUMCOINS; i ++){
            if(i + 1 != COUNTERFEIT_ID){
                listCoin.add(new Coin(i + 1, REAL_WEIGHT));
            }
            else{
                listCoin.add(new Coin(i + 1, FAKE_WEIGHT));
            }
        }

        System.out.println(String.format("\nWe have %d identical-looking coins but one of them is a counterfeit and weighs less than the others.", NUMCOINS));
        System.out.println(String.format("Using a balance scale, try to find the counterfeit coin by using the balance only %d times.\n", EXPECTED_TRIALS));

        double numWeighingCoins = NUMCOINS;
        ArrayList<Coin> listWeighingCoins = new ArrayList<>();
        for(Coin coin: listCoin) {
            listWeighingCoins.add(coin);
        }
        int WeighNumber = 1;


        while(numWeighingCoins != 1){
            ArrayList<Coin> group1 = new ArrayList<>();
            ArrayList<Coin> group2 = new ArrayList<>();
            ArrayList<Coin> group3 = new ArrayList<>();

            if(numWeighingCoins % 3 == 0 || numWeighingCoins % 3 == 1) {
                for(int i = 0; i < listWeighingCoins.size(); i ++){
                    if(i < (int)(numWeighingCoins / 3)) {
                        group1.add(listWeighingCoins.get(i));
                    }
                    else if(i < 2 * (int)(numWeighingCoins / 3)) {
                        group2.add(listWeighingCoins.get(i));
                    }
                    else {
                        group3.add(listWeighingCoins.get(i));
                    }
                }
            }
            else if(numWeighingCoins % 3 == 2) {
                for(int i = 0; i < listWeighingCoins.size(); i ++){
                    if(i < (int)((numWeighingCoins + 1) / 3)) {
                        group1.add(listWeighingCoins.get(i));
                    }
                    else if(i < 2 * (int)((numWeighingCoins + 1) / 3)) {
                        group2.add(listWeighingCoins.get(i));
                    }
                    else {
                        group3.add(listWeighingCoins.get(i));
                    }
                }
            }

            double alphaTotal = getTotalWeight(group1);
            double betaTotal = getTotalWeight(group2);

            listWeighingCoins.clear();
            if(alphaTotal == betaTotal) {
                for(int i = 0; i < group3.size(); i ++){
                    listWeighingCoins.add(group3.get(i));
                }
            }
            else if(alphaTotal > betaTotal) {
                for(int i = 0; i < group2.size(); i ++){
                    listWeighingCoins.add(group2.get(i));
                }
            }
            else if(betaTotal > alphaTotal) {
                for(int i = 0; i < group1.size(); i ++){
                    listWeighingCoins.add(group1.get(i));
                }
            }

            numWeighingCoins = listWeighingCoins.size();





            System.out.println(String.format("--------------------Weight Try #%d--------------------\n", WeighNumber));

            String outStr = "Left side group will consist of " + group1.size() + " coin(s) with numbers: \n";
            for(int i = 0; i < group1.size(); i ++){
                Coin coin = group1.get(i);
                if(i % 15 == 14) {
                    outStr += coin.getIdentifier() + "\n";
                }
                else {
                    outStr += coin.getIdentifier() + " ";
                }
            }
            System.out.println(outStr + "\n");

            outStr = "Right side group will consist of " + group2.size() + " coin(s) with numbers: \n";
            for(int i = 0; i < group2.size(); i ++){
                Coin coin = group2.get(i);
                if(i % 15 == 14) {
                    outStr += coin.getIdentifier() + "\n";
                }
                else {
                    outStr += coin.getIdentifier() + " ";
                }
            }
            System.out.println(outStr + "\n");


            if(alphaTotal == betaTotal) {
                System.out.println("Both sides were equal in weight so the counterfeit is amongst the unweighed coins.");
            }
            else if(alphaTotal > betaTotal) {
                System.out.println("Left side was heavier so the counterfeit is in the right side.");
            }
            else if(betaTotal > alphaTotal) {
                System.out.println("Right side was heavier so the counterfeit is in the left side.");
            }

            WeighNumber += 1;
        }
    }
}