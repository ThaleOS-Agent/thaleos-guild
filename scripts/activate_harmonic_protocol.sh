#!/bin/bash

echo "Initializing ThaleOS Harmonic Protocol..."

ROOT=~/ThaleOS_Project_Root/ThaleOS

cd $ROOT || exit

echo "Starting Memory Core..."
docker compose up -d redis postgres

echo "Starting FastAPI Orchestrator..."
cd core/orchestrator
uvicorn main:app --host 0.0.0.0 --port 9110 &

echo "Starting UTILIX Router..."
cd ../../utilix
python utilix_daemon.py &

echo "Launching Agent Scheduler..."
cd ../core/scheduler
python scheduler.py &

echo "Starting React Guild Console..."
cd ../../apps/guild-console
npm run dev &

echo "ThaleOS Harmonic Protocol Activated"