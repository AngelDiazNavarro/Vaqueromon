package Classes;
public abstract class mon {
    private final String name;
    
    private  int health;

    private int atk;

    private final Mon_type type;

    private int speed;

    private int defense;
    
    private final Moves move;


    public mon(String name, int health,int atk,int speed,int  defense, Mon_type type, Moves move) {
            this.name = name;
            setHealth(health);
            this.atk= atk;
            this.speed = speed;
            this.defense = defense;
            this.type = type;
            this.move = move;

    }   
    public String getName(){
        return name;
    }
    public int getHealth(){
        return health;
    }
    public void setHealth(int health){
        this.health = health;
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
    public Moves getMove(){
        return move;
    }
    public void takeDamege(int damage){
        setHealth(damage/defense*2);
    }
    
    }