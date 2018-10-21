package speakeasy;

import com.google.cloud.storage.Bucket;
import com.google.cloud.storage.BucketInfo;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import org.springframework.web.multipart.MultipartFile;

public class BucketStorageService
{

    // ensure that
    // GOOGLE_APPLICATION_CREDENTIALS env var points to the file

    public BucketStorageService()
    {
        //Storage storage = StorageOptions();
    }

    /**
     * Stores a file in the google cloud
     * @param file
     * @return
     */
    public String store(MultipartFile file)
    {

        return null;
    }

}
