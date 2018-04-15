package com.example.christian.imagesjov;

import android.content.Intent;
import android.graphics.Bitmap;
import android.icu.util.Output;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64;
import android.widget.TextView;

import com.android.volley.RequestQueue;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "----------------->";
    TextView mTextView;
    RequestQueue queue;
    // Instantiate the RequestQueue.
    String url ="http://drunk-or-not.kf7ndqdifu.eu-central-1.elasticbeanstalk.com/";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mTextView = (TextView) findViewById(R.id.main_text);
        //queue = Volley.newRequestQueue(this);
        //queue.add(stringRequest);
        //
        Intent pictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if(pictureIntent.resolveActivity(getPackageManager() != null)){
            startActivityForResult(pictureIntent, 1);  // Request code = request_image_capture
        }

    }

    private String getStringFromBitmap(Bitmap bitmapPicture) {
        /*
         * This functions converts Bitmap picture to a string which can be
         * JSONified.
         * */
        final int COMPRESSION_QUALITY = 100;
        String encodedImage;
        ByteArrayOutputStream byteArrayBitmapStream = new ByteArrayOutputStream();
        bitmapPicture.compress(Bitmap.CompressFormat.PNG, COMPRESSION_QUALITY,
                byteArrayBitmapStream);
        byte[] b = byteArrayBitmapStream.toByteArray();
        encodedImage = Base64.encodeToString(b, Base64.DEFAULT);
        return encodedImage;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent){
        if (requestCode == 1 && requestCode == RESULT_OK) {
            Bundle extra = intent.getExtras();
            Bitmap bitmap = (Bitmap) extra.get("data");

            try {
                URL url = new URL(this.url);

                HttpURLConnection connection = (HttpURLConnection) url.openConnection();

                connection.setRequestMethod("POST");
                OutputStream os = connection.getOutputStream();
                OutputStreamWriter osw = new OutputStreamWriter(os, "UTF-8");

                osw.write(getStringFromBitmap(bitmap));
                osw.flush();
                osw.close();

                //INPUT STUFF FRA STACKOVERFLOW: https://stackoverflow.com/questions/38046429/get-json-response-while-performing-post-request-with-httpurlconnection
                //GG WP
                InputStreamReader in = new InputStreamReader(connection.getInputStream());
                BufferedReader br = new BufferedReader(in);
                String txt = "";
                String response = "";

                while((txt = br.readLine()) != null) {
                    response += txt;
                }

                

            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}