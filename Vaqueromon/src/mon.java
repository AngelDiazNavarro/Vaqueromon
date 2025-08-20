
public abstract class mon {
    private final String name;
    
    private  int health;

    private int atk;

    private final Mon_type type;

    private int speed;

    private int defense;


    public mon(String name, int health,int atk,int speed,int  defense, Mon_type type) {
            this.name = name;
            this.health = health;
            this.atk= atk;
            this.speed = speed;
            this.defense = defense;
            this.type = type;

    }   
    public String getName(){
        return name;
    }
    public int health(){
        return health;
    }
    public int atk(){
        return atk;
    }
    public int speed(){
        return speed;
    }
    public int defense(){
        return defense;
    }
    public Mon_type type(){
        return type;
    }
}
