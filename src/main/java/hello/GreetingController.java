package hello;

import java.util.concurrent.atomic.AtomicLong;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GreetingController
{
    private static final String template = "Hello %s";

    @RequestMapping("/test")
    public SampleGreeter test(@RequestParam(value="name", defaultValue="test") String name)
    {
        return new SampleGreeter(123, String.format(template, name));
    }
}
