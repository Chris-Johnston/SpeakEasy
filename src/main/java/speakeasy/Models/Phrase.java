package speakeasy.Models;

public class Phrase
{
    public Phrase()
    {
        text = "Unset text.";
    }

    public Phrase(String content, int id)
    {
        text = content;
        this.id = id;
    }

    /**
     * The phrase text
     */
    public String text;

    /**
     * The phrase unique ID
     */
    public int id;
}
