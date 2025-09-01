package Classes;
public class mon {
    private final String name;
    
    private  int health;

    private int atk;

    private final Mon_type type;

    private int speed;

    private int def;
    
    private final Moves move;

    // constructor for mon class needs pojo 
    public mon(String name, int health,int atk,int speed,int  def, Mon_type type, Moves move) {
            this.name = name;
            setHealth(health);
            this.atk= atk;
            this.speed = speed;
            this.def = def;
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
    public int def(){
        return def;
    }
    public Mon_type type(){
        return type;
    }
    public Moves getMove(){
        return move;
    }
    //damage formula (could be reworked)
    public void takeDamege(int damage){
        setHealth(damage/def*2);
    }
    
    }