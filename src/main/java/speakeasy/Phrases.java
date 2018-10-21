package speakeasy;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import speakeasy.Models.Phrase;

import java.util.ArrayList;
import java.util.List;

/**
 * Define this as an API controller
 */
@RestController
public class Phrases
{
    private List<Phrase> phrases;

    /**
     * Constructor
     *
     * Initializes a hard-coded list of all phrases.
     */
    public Phrases()
    {
        phrases = new ArrayList<Phrase>();
        phrases.add(new Phrase("Test Phrase #1", 1));
        phrases.add(new Phrase("Test Phrase #2", 2));
        phrases.add(new Phrase("Test Phrase #3", 3));
        phrases.add(new Phrase("Test Phrase #4", 4));
    }

    private Phrase getDefaultPhrase()
    {
        return new Phrase("Default Phrase", -1);
    }

    /**
     * Gets a Phrase by a Phrase's ID.
     * @param id
     * @return
     */
    @RequestMapping("/phrase")
    public Phrase getPhrase(@RequestParam(value="id") int id)
    {
        if (phrases != null)
        {
            // get the matching phrase by ID
            for (Phrase p : phrases)
            {
                if (p.id == id)
                    return p;
            }
        }
        // return default error case
        return getDefaultPhrase();
    }

    /**
     * Gets a list of all the Phrases
     * @return A list containing all of the phrases
     */
    @RequestMapping("/phrases")
    public List<Phrase> getAllPhrases()
    {
        return phrases;
    }
}
