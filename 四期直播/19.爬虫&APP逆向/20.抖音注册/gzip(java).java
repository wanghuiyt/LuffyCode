import java.io.ByteArrayInputSteam;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.math.BigInteger;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.io.OutputStream;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;


public class Hello {
    public static void main(String[] args) throws IOException {
        // 压缩
        String data = "我是小明";
        System.out.println(Arrays.toString(data.getBytes()));
        ByteArrayInputSteam v0_1 = new ByteArrayInputSteam();
        GZIPInputStream v1 = new GZIPInputStream(v0_1);
        v1.write(data.getBytes());
        v1.close();
        byte[] arg6 = v0_1.toByteArray();
        System.out.println(Arrays.toString(arg6);

        // 解压缩
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ByteArrayInputSteam in = new ByteArrayInputSteam(arg6);
        GZIPInputStream unzip = new GZIPInputStream(in);
        byte[] buffer = new byte[256];
        int n;
        while((n = unzip.read(buffer)) >= 0){
            out.write(buffer, 0, n);
        }
        byte[] res = out.toByteArray();
        System.out.println(Arrays.toString(res));
        System.out.println(out.toString("UTF-8"));
    }
}



