package speakeasy;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.nio.file.Path;

/**
 * Handles uploading of audio files
 */
@Controller
public class AudioUploader
{
    private final StorageService storage;

    public AudioUploader()
    {
        storage = new StorageService();
    }

    @GetMapping("/sampleResult")
    public String testAudioResult()
    {
        return "This is a sample result";
    }

    @PostMapping(value = "/audio", consumes = {"multipart/form-data"})
    public String handleFileUpload(@RequestParam("file") @NotNull @NotBlank MultipartFile file)
    {
        // store the file w/ the storage service
        Path p = storage.store(file);

        if (p == null)
        {
            return "Uh-oh, couldn't store the file";
        }

        // (debugging) return the absolute path
        return p.toAbsolutePath().toString();

        //return "OK!";
    }
}
