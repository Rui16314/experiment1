// Chart.js for data visualization
// This would typically be loaded from CDN, but included here for completeness

// Simple chart implementation for the experiment
class SimpleChart {
    constructor(canvasId, options = {}) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.options = options;
        this.data = options.data || {};
    }
    
    render() {
        const { type, labels, datasets } = this.options;
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (type === 'bar') {
            this.renderBarChart(labels, datasets);
        }
    }
    
    renderBarChart(labels, datasets) {
        const width = this.canvas.width;
        const height = this.canvas.height;
        const padding = 40;
        const barWidth = (width - padding * 2) / labels.length / 2;
        
        // Draw axes
        this.ctx.beginPath();
        this.ctx.moveTo(padding, padding);
        this.ctx.lineTo(padding, height - padding);
        this.ctx.lineTo(width - padding, height - padding);
        this.ctx.strokeStyle = '#333';
        this.ctx.stroke();
        
        // Draw bars
        datasets.forEach((dataset, datasetIndex) => {
            this.ctx.fillStyle = dataset.backgroundColor || '#667eea';
            
            dataset.data.forEach((value, index) => {
                const x = padding + (index * barWidth * 2) + (datasetIndex * barWidth);
                const barHeight = ((value / Math.max(...dataset.data)) * (height - padding * 2)) * 0.8;
                
                this.ctx.fillRect(x, height - padding - barHeight, barWidth, barHeight);
                
                // Draw label
                this.ctx.fillStyle = '#333';
                this.ctx.fillText(value, x + barWidth/2 - 10, height - padding - barHeight - 10);
            });
        });
        
        // Draw labels
        this.ctx.fillStyle = '#333';
        labels.forEach((label, index) => {
            const x = padding + (index * barWidth * 2) + barWidth;
            this.ctx.fillText(label, x - 20, height - padding + 20);
        });
    }
}

// Initialize charts when page loads
document.addEventListener('DOMContentLoaded', function() {
    const chartElements = document.querySelectorAll('[data-chart]');
    
    chartElements.forEach(element => {
        const chartId = element.id;
        const chartType = element.dataset.chartType || 'bar';
        const chartData = JSON.parse(element.dataset.chartData || '{}');
        
        new SimpleChart(chartId, {
            type: chartType,
            ...chartData
        }).render();
    });
});
