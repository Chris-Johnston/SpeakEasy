package hello;

public class SampleGreeter
{
    private final int id;
    private final String content;

    public SampleGreeter(int id, String c)
    {
        this.id = id;
        this.content = c;
    }

    public int getId() { return id; }
    public String getContent() { return content; }
}
