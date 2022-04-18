import java.util.Random;

class Coin {
    int identifier;
    double weight;

    Coin(int identifier, double weight) {
        this.identifier = identifier;
        this.weight = weight;
    }

    int getIndentifier() {
        return this.identifier;
    }

    double getWeight() {
        return this.getWeight();
    }

    double getTotalWeight(Coin[] listCoin) {
        double totalWeight = 0;
        for(Coin coin: listCoin) {
            totalWeight += coin.getWeight()
        }
        return totalWeight;
    }
}

public class CounterfeitCoin {
    public static void main(String[] args) {
        
    }
}