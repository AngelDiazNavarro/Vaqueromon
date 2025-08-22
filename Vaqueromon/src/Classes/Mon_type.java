package Classes;
public enum  Mon_type {
    FIRE, WATER, GRASS;

    public String toString(){
        switch(this) {
            case FIRE: return "Fire";
            case WATER: return "Water";
            case GRASS: return "Grass";
            default: return "Unknown";
        }
    }
}
