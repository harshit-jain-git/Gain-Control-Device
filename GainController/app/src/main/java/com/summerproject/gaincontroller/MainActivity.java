package com.summerproject.gaincontroller;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ConnectException;
import java.net.Socket;

import static java.lang.Thread.sleep;

public class MainActivity extends AppCompatActivity {

    boolean flag = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // initiate the Seek bars
        final SeekBar simpleSeekBar1=findViewById(R.id.seekBar1);
        final SeekBar simpleSeekBar2=findViewById(R.id.seekBar2);
        final SeekBar simpleSeekBar3=findViewById(R.id.seekBar3);
        final SeekBar simpleSeekBar4=findViewById(R.id.seekBar4);
        final SeekBar simpleSeekBar5=findViewById(R.id.seekBar5);
        final SeekBar simpleSeekBar6=findViewById(R.id.seekBar6);
        final SeekBar simpleSeekBar7=findViewById(R.id.seekBar7);
        final SeekBar simpleSeekBar8=findViewById(R.id.seekBar8);

        simpleSeekBar1.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,
                                          boolean fromUser) {
                TextView gain_1=findViewById(R.id.gain_1);
                gain_1.setText("Gain: " + progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        simpleSeekBar2.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,
                                          boolean fromUser) {
                TextView gain_2=findViewById(R.id.gain_2);
                gain_2.setText("Gain: " + progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        simpleSeekBar3.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,
                                          boolean fromUser) {
                TextView gain_3=findViewById(R.id.gain_3);
                gain_3.setText("Gain: " + progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        simpleSeekBar4.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,
                                          boolean fromUser) {
                TextView gain_4=findViewById(R.id.gain_4);
                gain_4.setText("Gain: " + progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        simpleSeekBar5.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,
                                          boolean fromUser) {
                TextView gain_5=findViewById(R.id.gain_5);
                gain_5.setText("Gain: " + progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        simpleSeekBar6.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,
                                          boolean fromUser) {
                TextView gain_6=findViewById(R.id.gain_6);
                gain_6.setText("Gain: " + progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        simpleSeekBar7.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,
                                          boolean fromUser) {
                TextView gain_7=findViewById(R.id.gain_7);
                gain_7.setText("Gain: " + progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        simpleSeekBar8.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,
                                          boolean fromUser) {
                TextView gain_8=findViewById(R.id.gain_8);
                gain_8.setText("Gain: " + progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        final Thread network = new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("Thread started");
                try {
                    Socket s = new Socket("10.184.27.97", 7000);
                    DataOutputStream dos = new DataOutputStream(s.getOutputStream());
                    while (true) {
                        while (flag) {
                            // connect to the device and change the gain values.
                            // get progress value from the Seek bar
                            int seekBarValue1 = simpleSeekBar1.getProgress();
                            int seekBarValue2 = simpleSeekBar2.getProgress();
                            int seekBarValue3 = simpleSeekBar3.getProgress();
                            int seekBarValue4 = simpleSeekBar4.getProgress();
                            int seekBarValue5 = simpleSeekBar5.getProgress();
                            int seekBarValue6 = simpleSeekBar6.getProgress();
                            int seekBarValue7 = simpleSeekBar7.getProgress();
                            int seekBarValue8 = simpleSeekBar8.getProgress();

                            JSONArray arr = new JSONArray();
                            arr.put(seekBarValue1);
                            arr.put(seekBarValue2);
                            arr.put(seekBarValue3);
                            arr.put(seekBarValue4);
                            arr.put(seekBarValue7);
                            arr.put(seekBarValue6);
                            arr.put(seekBarValue5);
                            arr.put(seekBarValue8);
                            System.out.println(arr.toString());

                            dos.writeBytes(arr.toString());
                            flag = false;
                        }
                        sleep(500);
                    }
                }
                catch (ConnectException e) {
                    e.printStackTrace();
                    finish();
                    System.exit(0);
                } catch (IOException e) {
                    e.printStackTrace();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        network.start();

        Button button= findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // send these values to pi
                System.out.println("Button Clicked");
                flag = true;
            }
        });
    }
}
