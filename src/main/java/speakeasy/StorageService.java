package speakeasy;

import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class StorageService
{
    public StorageService()
    {

    }


    /**
     * Gets a temporary directory to save files into
     * @return
     */
    private Path getTemporaryDirectory()
    {
        try
        {
            return Files.createTempDirectory("speakeasy");
        }
        catch (IOException e)
        {
            System.out.println("Tried to create a temporary directory but encountered IOException: " + e.toString());
            return null;
        }
    }

    /**
     * Gets the temporary directory to save a file under.
     * If error, returns null
     * @param filename the file name to save
     * @return the full path under the temporary directory
     */
    private Path getTemporaryPathForFile(String filename)
    {
        Path p = getTemporaryDirectory();
        // if error, return null
        if (p == null) return null;

        return p.resolve(filename);
    }

    /**
     * Stores a multipart file in the temporary location on disk
     * @param file the file to store
     * @return the path of the file stored on the disk. returns null if error
     */
    Path store(MultipartFile file)
    {
        if (file == null)
        {
            System.out.println("the file supplied was null");
            return null;
        }


        String filename = StringUtils.cleanPath(file.getOriginalFilename());
        try
        {
            if (file.isEmpty())
            {
                // file was empty
                return null;
            }
            if (filename.contains(".."))
            {
                // don't allow traversal in the file name
                return null;
            }
            InputStream stream = file.getInputStream();
            Path p = getTemporaryPathForFile(filename);
            if (p == null)
            {
                System.out.println("path for the file " + filename + " could not be determined");
                return null;
            }
            // copy the file to the path
            Files.copy(stream, p);
            // return it's path
            return p;
        }
        catch (IOException e)
        {
            // couldn't store the file for some reason, just print out to the console
            System.out.println("Encountered an IOException when trying to store the file. " + e);
        }
        // no path
        return null;
    }
}
